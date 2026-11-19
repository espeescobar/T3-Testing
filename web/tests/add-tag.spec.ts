// spec: tests/plan-final.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

const apiBaseURL = 'http://127.0.0.1:5000';

test.describe('Etiquetas', () => {
  test(
    'Agregar una etiqueta nueva desde el detalle',
    { tag: ['@ia', '@copilot'] },
    async ({ page, request }) => {
      const unique = Date.now();
      const quoteText = `Frase para agregar etiqueta ${unique}`;
      const source = `Fuente para agregar etiqueta ${unique}`;
      const tagName = `etiqueta-playwright-${unique}`;
      let quoteId: string | undefined;
      let tagId: string | undefined;

      try {
        // 1. Crear la frase por API con Marie Curie y abrir su detalle.
        const createResponse = await request.post(`${apiBaseURL}/quotes/add`, {
          data: {
            quote: quoteText,
            character: 'Marie Curie',
            source,
            tags: [],
          },
        });
        expect(createResponse.status()).toBe(201);

        const createdQuote = await createResponse.json();
        if (typeof createdQuote.id !== 'string' || !createdQuote.id) {
          throw new Error('POST /quotes/add did not return a quote id');
        }
        quoteId = createdQuote.id;

        await page.goto(`/quotes/${quoteId}`);

        // 2. Agregar una etiqueta única al detalle.
        await page.getByRole('button', { name: 'Add Tag' }).click();
        const dialog = page.getByRole('dialog');
        await dialog.getByRole('textbox', { name: 'chile, humor, tv' }).fill(tagName);

        const addTagResponsePromise = page.waitForResponse(
          (response) =>
            response.url() === `${apiBaseURL}/quotes/${quoteId}/tags` &&
            response.request().method() === 'POST',
        );
        await dialog.getByRole('button', { name: 'Agregar etiquetas' }).click();

        const addTagResponse = await addTagResponsePromise;
        expect(addTagResponse.status()).toBe(201);
        const createdTags: Array<{ id: string; name: string }> = await addTagResponse.json();
        expect(createdTags).toHaveLength(1);
        const createdTag = createdTags[0];
        if (!createdTag?.id) {
          throw new Error('POST /quotes/<id>/tags did not return a tag id');
        }
        tagId = createdTag.id;

        await expect(page.getByText('Etiquetas añadidas exitosamente', { exact: true })).toBeVisible();
        await expect(page.getByText(tagName, { exact: true })).toHaveCount(1);

        // 3. Recargar y verificar que la etiqueta persistió.
        await page.reload();
        await expect(page.getByText(tagName, { exact: true })).toHaveCount(1);
      } finally {
        try {
          // 4. Limpiar primero la frase y luego la etiqueta creada.
          if (quoteId) {
            const deleteQuoteResponse = await request.delete(
              `${apiBaseURL}/quotes/delete/${quoteId}`,
            );
            expect(deleteQuoteResponse.ok()).toBeTruthy();
          }
        } finally {
          if (tagId) {
            const deleteTagResponse = await request.delete(
              `${apiBaseURL}/tags/delete/${tagId}`,
            );
            expect(deleteTagResponse.ok()).toBeTruthy();
          }
        }
      }
    },
  );
});
