// spec: tests/plan-final.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Colección: búsqueda y filtros', () => {
  test(
    'Buscar por texto filtra las tarjetas y limpiar las restaura',
    { tag: ['@ia', '@copilot'] },
    async ({ page }) => {
      // 1. Abrir /quotes y escribir "shoulders" en "Buscar frases...".
      await page.goto('/quotes');

      const grid = page.getByTestId('quotes-grid');
      const search = page.getByPlaceholder('Buscar frases...');

      await search.fill('shoulders');

      await expect(
        grid.getByText('If I have seen further it is by standing on the shoulders of Giants.', { exact: true }),
      ).toBeVisible();
      await expect(
        grid.getByText('Nothing in life is to be feared', { exact: false }),
      ).toHaveCount(0);

      // 2. Borrar el texto del campo.
      await search.clear();

      await expect(
        grid.getByText('If I have seen further it is by standing on the shoulders of Giants.', { exact: true }),
      ).toBeVisible();
      await expect(
        grid.getByText('Nothing in life is to be feared', { exact: false }),
      ).toBeVisible();
    },
  );
});
