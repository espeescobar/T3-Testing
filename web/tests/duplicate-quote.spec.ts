// spec: tests/plan-final.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

const apiBaseURL = 'http://127.0.0.1:5000';
const duplicateQuote = 'Do what you can, with what you have, where you are.';

test.describe('Creación de frases', () => {
  test(
    'Frase duplicada es rechazada',
    { tag: ['@ia', '@copilot'] },
    async ({ page, request }) => {
      await page.goto('/');
      await page.getByRole('button', { name: 'Nueva frase' }).click();

      // El popover del combobox también tiene role="dialog"; se acota por nombre.
      const dialog = page.getByRole('dialog', { name: 'Nueva frase' });

      // 1. Completar el formulario con la frase seed, Theodore Roosevelt y su fuente.
      await dialog.getByRole('textbox', { name: 'Frase' }).fill(duplicateQuote);
      await dialog.locator('button[role="combobox"]').click();
      await page.getByRole('option', { name: 'Theodore Roosevelt' }).click();
      await dialog.getByRole('textbox', { name: 'Fuente' }).fill('Theodore Roosevelt');

      // 2. Enviar el duplicado y comprobar la respuesta y el estado de la UI.
      const addResponsePromise = page.waitForResponse(
        (response) =>
          response.url() === `${apiBaseURL}/quotes/add` &&
          response.request().method() === 'POST',
      );
      await dialog.getByRole('button', { name: 'Añadir' }).click();

      const addResponse = await addResponsePromise;
      expect(addResponse.status()).toBe(409);
      await expect(dialog.getByText('Error al añadir la frase.', { exact: true })).toBeVisible();
      await expect(dialog.getByText(/La cita ya existe\./)).toBeVisible();
      await expect(dialog).toBeVisible();

      const quotesResponse = await request.get(`${apiBaseURL}/quotes`);
      expect(quotesResponse.ok()).toBeTruthy();
      const quotes = await quotesResponse.json();
      expect(quotes.filter((quote: { quote: string }) => quote.quote === duplicateQuote)).toHaveLength(1);
    },
  );
});
