# Test Cases: LT-98511 - Adjust Lesson Duration by Course

## Suite: Adjust Lesson Duration by Course (LT-98511)

### TC-01 - Location Course duration field - Config ON displays optional field and saves value

Verify Riso can configure a Location Course duration and reload the saved value.

### TC-02 - Location Course duration field - Blank default remains blank

Verify the field is optional and blank by default.

### TC-03 - Lesson creation - Location Course duration overrides 80-minute timeslot

Verify a 50-minute Location Course overrides an 80-minute timeslot.

### TC-04 - Lesson creation - Blank Location Course duration falls back to timeslot

Verify the existing timeslot-derived duration remains when no course duration is configured.

### TC-05 - Lesson creation - No course duration and no timeslot keeps existing default/manual behavior

Verify no forced course duration is applied when no source exists.

### TC-06 - Lesson creation - Manual Duration, Start Time, and End Time edits are retained until source change

Verify manual overrides are still possible.

### TC-07 - Lesson creation - Timeslot change recalculates after manual override

Verify changing Timeslot after manual edits recalculates the form.

### TC-08 - Lesson creation - Location Course change recalculates and config OFF preserves old behavior

Verify changing course recalculates, and disabled config hides the feature for non-Riso/OFF scenarios.

### TC-09 - Lesson creation - Tenant without Timeslot feature still applies Location Course duration

Verify tenant/org flows that do not use Timeslot can still apply Location Course duration from course selection, and blank course duration preserves the existing manual/default duration behavior.
