# Four home access revisions

- Three Bedroom Compact Duplex: remove the first-floor kitchen, retain a clear
  4 x 6 ft entrance lobby, and mark the entrance from the front access balcony.
  The ground-floor kitchen stays. Cover/website copy reflects the single kitchen.
- Three Bedroom Courtyard Home: place a 10 x 6 ft kitchen on the rear 40 ft wall,
  with its own open connection to living. A separate 5 x 6 ft lobby connects
  living to the 5 x 6 ft bathroom, so bathroom access does not pass through kitchen.
- Two Bedroom Living, 40 ft option: use two gross 14 x 12 ft bedroom suites,
  with 6 x 4 ft ensuites on the rear long wall. Living accesses bedroom 2, and
  D7 is a 3 ft internal door from bedroom 2 to bedroom 1. Remove the outside-only
  bedroom entrance. Keep the 12 x 12 ft end living/kitchen and the 44 ft option.
- Silver One Bedroom Home: move the sink/prep/hob counter to the front window
  wall and open its connection to the service passage.

Shared bed checks retain 5 x 6.5 ft beds, solid headboards and at least 2.5 ft
side/foot access. All building footprints and PDF page counts are retained.
Transparent logos, exterior concepts and material standards remain in the PDFs.

Rebuild with `python scripts/refresh_home_access.py` using the bundled runtime
and `tmp/python-deps` on PYTHONPATH. The script updates all four website files,
descriptions, cache revisions and manifests; review images are in ignored
`tmp/pdfs/home-access`. The collection remains 30 distinct PDFs / 359 pages.
