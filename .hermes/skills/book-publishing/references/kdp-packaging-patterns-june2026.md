# KDP Package Build & Cleanup Pattern (June 2026)

## Problem
KDP zips accumulate with inconsistent naming (PascalCase, kebab-case, legacy prefixes, archived copies), inflating count 2-3x.

## Canonical Structure
`KDP_Packages/PascalName/PascalName_KDP_PACKAGE.zip`
Each package: Cover.jpg, Back_Cover.txt, Author_Bio.txt, Description.txt, Keywords.txt, Title.txt, Infographic.png, Author_Photo.jpg, PascalName.epub

## Cleanup Steps
1. `find ~/books -name "*.zip" -not -path "*/_archived/*"`
2. Keep only PascalCase in KDP_Packages/
3. Delete ALL other zips
4. Build packages by collecting files from book dirs
5. `find ~/books -type d -empty -delete`

## Book Dirs (20 books, June 2026)
Series dirs: No_Blue_Sky_Series/ (5), Age_of_Lightships_Series/ (4), Lunar_Foundation_Series/ (4), Business_Series/ (3), Cindy_Lou_Legal_Capers/ (3), Tomorrow_Remembered/ (1)
Exclude: KDP_Packages/, books-section/, hermes_publish/, scripts/, _SHARED_QR/, _archived/

## Metadata Prefix Inconsistency
- NBS: PascalCase prefix | AL: kebab prefix | LF: PascalCase | Business: mixed | Cindy Lou: generic

## KDP_PACKAGE Subdirs ≠ Canonical
Per-book KDP_PACKAGE/ dirs are NOT the canonical package. Canonical = KDP_Packages/PascalName/.
