import { test, expect, request } from '@playwright/test';

const apiContext = await request.newContext({
  baseURL: 'http://localhost:5000',
  extraHTTPHeaders: { 'Content-Type': 'application/json' },
});

// Flujo: enviar el formulario de "Nueva frase" incompleto muestra un error y no crea nada.
test('formulario incompleto muestra error y no crea la frase', { tag: '@manual' }, async ({ page }) => {
  const text = 'Frase incompleta e2e';
  await page.goto('/');
  await page.getByRole('button', { name: 'Nueva frase' }).click();
  await page.getByRole('textbox', { name: 'Frase' }).fill(text);
  await page.getByRole('button', { name: 'Añadir' }).click();

  await expect(page.getByText('Error al añadir la frase.')).toBeVisible();
  await expect(page.getByText(/Faltan campos obligatorios/)).toBeVisible();

  // La frase no debe existir en el backend (no hay nada que limpiar).
  const quotes = await (await apiContext.get('/quotes')).json();
  expect(quotes.some((q: any) => q.quote === text)).toBe(false);
});

// Flujo: con "Psycho Killer Mode" activo, eliminar una frase desde el grid y confirmar.
test('eliminar una frase desde el grid con el modo eliminar', { tag: '@manual' }, async ({ page }) => {
  const text = 'Frase para eliminar e2e';
  const created = await apiContext.post('/quotes/add', {
    data: { quote: text, character: 'Marie Curie', source: 'E2E', tags: [] },
  });
  const { id } = await created.json();

  try {
    await page.goto('/quotes');
    const card = page.locator('[data-slot="card"]').filter({ hasText: text });
    await expect(card).toBeVisible();

    await page.getByRole('switch').click();
    await card.getByRole('button').click();
    await expect(page.getByText('será eliminada permanentemente')).toBeVisible();
    await page.getByRole('button', { name: 'Eliminar' }).click();

    await expect(card).toHaveCount(0);
    expect((await apiContext.get(`/quotes/${id}`)).status()).toBe(404);
  } finally {
    await apiContext.delete(`/quotes/delete/${id}`); // limpieza si el test falló antes de borrar
  }
});

// Bug: al elegir un personaje después de buscar texto, el filtro de búsqueda se ignora.
// Esperado: solo la frase de Uncle Iroh que contiene "Life happens". Actual: aparecen las 2 de Iroh.
test('bug: filtrar por personaje ignora el texto de búsqueda', { tag: '@manual' }, async ({ page }) => {
  await page.goto('/quotes');
  const grid = page.getByTestId('quotes-grid');
  await expect(grid.getByText('Life is like riding a bicycle')).toBeVisible();

  await page.getByPlaceholder('Buscar frases...').fill('Life happens');
  await page.getByRole('combobox').click();
  await page.getByRole('option', { name: 'Uncle Iroh' }).click();

  await expect(grid.getByText('Life happens wherever you are')).toBeVisible();
  await expect(grid.getByText('Sometimes the best way to solve')).toHaveCount(0);
});