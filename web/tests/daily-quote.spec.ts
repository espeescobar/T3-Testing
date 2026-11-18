// spec: tests/plan-final.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Frase diaria', () => {
  test(
    'La frase diaria muestra frase, personaje y etiquetas',
    { tag: ['@ia', '@copilot'] },
    async ({ page }) => {
      // 1. Abrir / y capturar la respuesta de GET /quotes/daily que usa la propia página
      const dailyResponse = page.waitForResponse(
        (res) => res.url().endsWith('/quotes/daily') && res.request().method() === 'GET'
      );
      await page.goto('/');
      const quote = await (await dailyResponse).json();

      // Frase
      await expect(page.getByRole('heading', { name: quote.quote, exact: true })).toBeVisible();

      // Personaje (y fuente si es distinta)
      const attribution =
        quote.source === quote.character.name
          ? `- ${quote.character.name}`
          : `- ${quote.character.name} (${quote.source})`;
      await expect(page.getByText(attribution, { exact: true })).toBeVisible();

      // Etiquetas
      for (const tag of quote.tags) {
        await expect(page.getByText(tag.name, { exact: true })).toBeVisible();
      }

      // Botón para agregar etiquetas
      await expect(page.getByRole('button', { name: 'Add Tag' })).toBeVisible();
    }
  );
});