# Filename Mismatch Patterns — Book Deliverable Sources

When copying latest book deliverables into structured series directories,
the filenames in `publishing_output/packages/`, `publishing_output/`, and
`publishing_output/covers/` often differ from each other. This reference
documents all known mismatches so future agents can match files correctly.

## No Blue Sky Series

| Book | Package zip | Epub (packages/) | Print PDF | Cover |
|------|-------------|-------------------|-----------|-------|
| 1 - Built from Dust | `No_Blue_Sky_1_Built_from_Dust_Publishing_Package.zip` | `No_Blue_Sky_1_Built_from_Dust.epub` | `No_Blue_Sky_1_Built_from_Dust_Print_Ready.pdf` | `NBS_1_Built_from_Dust_Cover.png` |
| 2 - The Oxygen Gamble | `No_Blue_Sky_2_The_Oxygen_Gamble_Publishing_Package.zip` | `No_Blue_Sky_2_The_Oxygen_Gamble.epub` | `No_Blue_Sky_2_Oxygen_Gamble_Print.pdf` *(note: no "The_" between 2 and Oxygen)* | `NBS_2_Oxygen_Gamble_Cover.png` |
| 3 - Rivers Under Mars | `No_Blue_Sky_3_Rivers_Under_Mars_Publishing_Package.zip` | `No_Blue_Sky_3_Rivers_Under_Mars.epub` | `No_Blue_Sky_3_Rivers_Under_Mars_Print.pdf` | `NBS_3_Rivers_Under_Mars_Cover.png` |
| 4 - The Red Charter | `No_Blue_Sky_4_Red_Charter_Publishing_Package.zip` | `No_Blue_Sky_4_Red_Charter.epub` | `No_Blue_Sky_4_Red_Charter_Print.pdf` | `NBS_4_Red_Charter_Cover.png` |
| 5 - The First Martian Nation | `No_Blue_Sky_5_First_Martian_Nation_Publishing_Package.zip` | `No_Blue_Sky_5_First_Martian_Nation.epub` | `No_Blue_Sky_5_First_Martian_Nation_Print.pdf` | `NBS_5_First_Martian_Nation_Cover.png` |

**Key mismatches:**
- Book 2 print PDF drops "The_" from the title compared to the epub
- Cover files use `NBS_` prefix (short series code) while everything else uses `No_Blue_Sky_`
- Package zips use `Publishing_Package.zip` suffix, not `KDP_PACKAGE.zip`

## The Lunar Foundation Series

*(Series directory: `Lunar_Foundation_Series/` — note: file names still use `The_Lunar_Foundation_` prefix in packages/zips)*

| Book | Package zip | Epub (packages/) | Print PDF | Cover |
|------|-------------|-------------------|-----------|-------|
| 1 - Moon Rock | `The_Lunar_Foundation_1_Moon_Rock_Publishing_Package.zip` | `The_Lunar_Foundation_1_Moon_Rock.epub` | `Lunar_Foundation_1_Moon_Rock_Print.pdf` | `LF_1_Moon_Rock_Cover.png` |
| 2 - Mooncoming | `The_Lunar_Foundation_2_Mooncoming_Publishing_Package.zip` | `The_Lunar_Foundation_2_Mooncoming.epub` | `Lunar_Foundation_2_Mooncoming_Print.pdf` | `LF_2_Mooncoming_Cover.png` |
| 3 - Waters End | `The_Lunar_Foundation_3_Waters_End_Publishing_Package.zip` | `The_Lunar_Foundation_3_Waters_End.epub` | `Lunar_Foundation_3_Waters_End_Print.pdf` | `LF_3_Waters_End_Cover.png` |
| 4 - Waters Horizon | *(no package zip exists)* | `Lunar_Fnd_4_Waters_Horizon.epub` *(note: "Fnd" abbreviation, no "The_Lunar_")* | `Lunar_Foundation_4_Waters_Horizon_Print.pdf` | `LF_4_Waters_Horizon_Cover.png` *(generated May 2026 — see book-cover-design skill)* |

**Key mismatches:**
- Package zip and the packages/ epub use full `The_Lunar_Foundation_N_` prefix, but the raw EPUB in publishing_output/ uses `Lunar_Fnd_N_` (abbreviated)
- Print PDFs drop the `The_` prefix compared to package zips
- Cover files use `LF_N_` prefix (short series code)
- Book 4 has NO package zip and NO cover — it's an incomplete book

## Owner's Manual for AI Agents

| File type | Filename |
|-----------|----------|
| Package zip (packages/) | `Owners_Manual_AI_Agents_Publishing_Package.zip` |
| Package zip (root) | `Owners_Manual_AI_Agents_KDP_PACKAGE.zip` |
| Epub (packages/) | `Owners_Manual_AI_Agents.epub` |
| Print PDF (packages/) | `Owners_Manual_AI_Agents_Print_Ready.pdf` |
| Cover | `Owners_Manual_AI_Agents_Cover.png` |

## Tomorrow Remembered

| File type | Source path |
|-----------|-------------|
| Package zip | `Tommrow_Remembered/output/Tomorrow_Remembered_KDP_PACKAGE.zip` |
| Epub | `Tommrow_Remembered/output/Tomorrow_Remembered.epub` |
| Print PDF | `Tommrow_Remembered/output/Tomorrow_Remembered_Print_6x9.pdf` |
| Cover | `Tommrow_Remembered/output/Tomorrow_Remembered_Cover.png` |

## Cover Naming Convention

Covers in `publishing_output/covers/` use a short series code prefix:

| Series | Prefix | Example |
|--------|--------|---------|
| No Blue Sky | `NBS_N_Title_Cover.png` | `NBS_1_Built_from_Dust_Cover.png` |
| The Lunar Foundation | `LF_N_Title_Cover.png` | `LF_1_Moon_Rock_Cover.png` |
| Standalone | `Title_Cover.png` | `Owners_Manual_AI_Agents_Cover.png` |

Some covers also have a `_raw.png` variant (the 1024x1024 generated art before
typography was applied). These are NOT the final cover — use the `_Cover.png` file.
