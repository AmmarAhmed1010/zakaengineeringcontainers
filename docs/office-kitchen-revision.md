# Open office kitchen revision

All nine original office catalogues use Kitchen in the plan and room schedule,
including both upper floors of the two-storey offices. Sink and hob counters sit
against the outer wall. Open kitchen sides replace unnecessary internal doors.
The upper landing and shared corridor connect without competing door swings.

The compact single-cabin office borrows a 2 ft strip from the office to provide
a 6 x 4 ft kitchen with a 2 ft counter and 4 ft approach. The overall footprint
stays 8 x 20 ft. The field-office counter is against the rear of its 4 x 8 ft bay,
leaving a 6 ft approach. In the twin-cabin office the kitchen and compact washroom
move to the outer left service bank so both private offices remain reachable.
The front entrance moves from 8.5 ft to 8 ft along the facade, directly into the
first office, with a separate internal door to the second office.
Upper exterior doors align with the open circulation side of the service bay.

The three newer office catalogues already have kitchens and clear entrance routes;
their layouts, including the enclosed passage-accessed executive-suite kitchen,
are retained. Shared material-specification headings may still refer to a
kitchen/pantry; floor-plan room labels and schedules all say Kitchen.

Regenerate this revision with `python scripts/refresh_office_kitchens.py` using the
bundled Python runtime and `tmp/python-deps` on PYTHONPATH. The script preserves
all cover, exterior and material-standard pages, synchronizes website download
copies, updates hashes/cache revisions and writes `office-kitchen-audit.json`.
The geometric check rejects any door swing crossing a kitchen counter and any
counter approach below 3 ft. Rendered review pages are in ignored
`tmp/pdfs/office-kitchens`.
