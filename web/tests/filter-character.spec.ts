// spec: tests/plan-final.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Colección: búsqueda y filtros', () => {
  test(
    'Filtrar por personaje y volver a Todos',
    { tag: ['@ia', '@copilot'] },
    async ({ page }) => {
      await page.goto('/quotes');

      const grid = page.getByTestId('quotes-grid');
      // El botón que abre el combobox (el campo de búsqueda del popover también
      // tiene role="combobox", por eso se apunta al botón y no al rol a secas).
      const characterTrigger = page.locator('button[role="combobox"]');

      // 1. Abrir el combobox y elegir "Elend Venture".
      await characterTrigger.click();
      await page.getByRole('option', { name: 'Elend Venture' }).click();

      await expect(
        grid.getByText('In the end, they will kill us. But first, they shall fear us!', { exact: true }),
      ).toBeVisible();
      await expect(
        grid.getByText('Do what you can, with what you have, where you are.', { exact: true }),
      ).toHaveCount(0);

      // 2. Abrir el combobox y elegir "Todos".
      await characterTrigger.click();
      await page.getByRole('option', { name: 'Todos' }).click();

      await expect(
        grid.getByText('Do what you can, with what you have, where you are.', { exact: true }),
      ).toBeVisible();
    },
  );
});