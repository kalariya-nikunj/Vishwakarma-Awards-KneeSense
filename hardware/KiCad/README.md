# Supplied hardware project

`Prototype_KneeSense_V1/` contains the supplied KiCad project tree, copied with original names and contents. Open `Prototype_KneeSense_V1.kicad_pro` in that directory. Keep `fp-lib-table`, `libraries/`, and `3dmodels/` together; the inspected custom footprint and model paths use `${KIPRJMOD}`.

Multiple Gerber ZIP variants, an extracted `gerbers/` directory, historical backup ZIPs, and a nested `kicad project/` are preserved. Their presence does not identify which revision was fabricated or approved. Confirm the intended board/export revision before ordering fabrication; no design-rule or manufacturing checks were performed during import.

The bundled Adafruit reference folder includes its original `license.txt` and `README.md`. Its `Adafruit SDIO microSD.sch` is only 7 bytes and contains `<?xml`, so it appears incomplete. It is preserved as supplied and must not be relied on as a complete reference schematic. This is separate from the main `Prototype_KneeSense_V1.kicad_sch` file.

KiCad local preference files (`.kicad_prl`) and historical backups are included to preserve the supplied collection. The working prototype's relationship to each archived design still needs documentation.
