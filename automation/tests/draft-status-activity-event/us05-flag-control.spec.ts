import { test, expect } from '@playwright/test';
import {
  sfLogin,
  sfNavigateTo,
  waitForPageReady,
  deepClickButton,
} from '../../helpers/sf-helpers';

const TENANT = 'staging';
const ORG = 'sandbox';
const ROLE = 'admin';
const OBJECT = 'MANAERP__Activity_Event__c';

test.describe('US05 — Flag Control', () => {
  test.beforeEach(async ({ page }) => {
    await sfLogin(page, TENANT, ORG, ROLE);
  });

  // PX-18448
  test('PX-18448: Flag ON — Draft option available in Status', async ({ page }) => {
    // Precondition: feature flag is enabled (default on staging)
    await sfNavigateTo(page, OBJECT);
    await deepClickButton(page, 'New');
    await waitForPageReady(page);
    await page.getByRole('heading', { name: 'Create Activity Event' }).waitFor({ timeout: 15_000 });

    const statusGroup = page.getByRole('radiogroup', { name: 'Activity Event Status' });
    await expect(statusGroup).toBeVisible();

    const draftRadio = statusGroup.getByRole('radio', { name: 'Draft' });
    await expect(draftRadio).toBeVisible();
  });

  // PX-18447
  test('PX-18447: Flag OFF — Draft option hidden from Status', async ({ page }) => {
    // NOTE: This test requires the feature flag to be OFF.
    // On staging the flag is typically ON, so this test should be run
    // after manually disabling the flag or on a separate org.
    test.skip(true, 'Requires feature flag to be OFF — toggle before running');

    await sfNavigateTo(page, OBJECT);
    await deepClickButton(page, 'New');
    await waitForPageReady(page);
    await page.getByRole('heading', { name: 'Create Activity Event' }).waitFor({ timeout: 15_000 });

    const statusGroup = page.getByRole('radiogroup', { name: 'Activity Event Status' });
    const draftRadio = statusGroup.getByRole('radio', { name: 'Draft' });
    await expect(draftRadio).toHaveCount(0);
  });
});
