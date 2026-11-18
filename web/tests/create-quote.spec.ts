// spec: tests/plan-final.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

const apiBaseURL = 'http://127.0.0.1:5000';

test.describe('Creación de frases', () => {
  test(
    'Crear frase con un personaje nuevo',
    { tag: ['@ia', '@copilot'] },
    async ({ page, request }) => {
      const unique = Date.now();
      const quoteText = `Frase creada por Playwright ${unique}`;
      const characterName = `Personaje Playwright ${unique}`;
      const source = `Fuente Playwright ${unique}`;
      const tagName = `etiqueta-playwright-${unique}`;
      let quoteId: string | undefined;
      let characterId: string | undefined;
      let tagId: string | undefined;

      try {
        await page.goto('/quotes');
        await page.getByRole('button', { name: 'Nueva frase' }).click();

        const dialog = page.getByRole('dialog');
        await dialog.getByRole('textbox', { name: 'Frase' }).fill(quoteText);

        // El botón que abre el combobox está dentro del diálogo...
        await dialog.locator('button[role="combobox"]').click();
        // ...pero el popover se renderiza en un portal fuera del diálogo,
        // por eso estos dos locators van con page y no con dialog.
        await page.locator('input[role="combobox"]').fill(characterName);
        // La app renderiza la opción "Create ..." dos veces (CommandEmpty y el grupo); ambas hacen lo mismo.
        await page.getByText(`Create "${characterName}"`, { exact: true }).first().click();
        await dialog.getByLabel('Fuente').fill(source);
        await dialog.getByLabel('Etiquetas').fill(tagName);

        const addResponsePromise = page.waitForResponse((response) =>
          response.url() === `${apiBaseURL}/quotes/add` && response.request().method() === 'POST',
        );

        await dialog.getByRole('button', { name: 'Añadir' }).click();

        const addResponse = await addResponsePromise;
        expect(addResponse.ok()).toBeTruthy();

        // Ids para la limpieza (salen de la respuesta de la API)
        const createdQuote = await addResponse.json();
        quoteId = createdQuote.id;
        characterId = createdQuote.character.id;
        tagId = createdQuote.tags?.[0]?.id;
        expect(quoteId).toBeTruthy();
        expect(characterId).toBeTruthy();

        await expect(page.getByText('Frase añadida exitosamente', { exact: true })).toBeVisible();
        await page.getByRole('button', { name: 'Ver' }).click();

        await expect(page.getByRole('heading', { name: quoteText, exact: true })).toBeVisible();
        await expect(page.getByText(`- ${characterName} (${source})`, { exact: true })).toBeVisible();
        await expect(page.getByText(tagName, { exact: true })).toBeVisible();

        // El personaje nuevo aparece como opción del filtro en /quotes
        await page.goto('/quotes');
        await page.locator('button[role="combobox"]').click();
        await expect(page.getByRole('option', { name: characterName })).toBeVisible();
      } finally {
        // Limpieza: primero la frase (la API no deja borrar un personaje con frases),
        // luego el personaje y la etiqueta, que quedan sueltos.
        if (quoteId) {
          await request.delete(`${apiBaseURL}/quotes/delete/${quoteId}`);
        }
        if (characterId) {
          await request.delete(`${apiBaseURL}/characters/delete/${characterId}`);
        }
        if (tagId) {
          await request.delete(`${apiBaseURL}/tags/delete/${tagId}`);
        }
      }
    },
  );
});