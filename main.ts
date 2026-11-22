// Entry program for "Sum up 22 November's world news in one image"
// (make.fun, news-image-20261122). Node 22, standard library only.
//
// The image is the front page this repository draws for Sunday
// 22 November 2026: COP31 collapses in Antalya, a Russian drone hits
// a Kyiv apartment block, Mexico captures 'El Chapo Isidro', Iran
// strikes a Bahrain site and tankers near Hormuz, the World Court
// rules on the Rohingya, US stocks fall into correction, NATO vows
// to defend Poland, BepiColombo reaches Mercury, and a factory fire
// in Indonesia.
//
// The image itself is drawn in code by generate.py (PIL shapes and
// text, no photos or stock art) and stored beside this file as
// entry.png. This program's job is to place exactly those bytes at
// /output/entry.png, after checking the file is a whole, in-limits
// PNG:
//  - PNG signature 89 50 4E 47 0D 0A 1A 0A
//  - width and height from the IHDR chunk, each at most 1024
//  - file size at most 1 MiB (1048576 bytes)
//  - the IEND chunk is present, so the image is complete
// It writes the same bytes on every run: the output is deterministic.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message) {
  throw new Error(`entry.png failed its checks: ${message}`);
}

function checkPng(bytes) {
  if (bytes.length > MAX_BYTES) fail(`too large: ${bytes.length} bytes`);
  if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail('not a PNG file');
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width === 0 || height === 0 || width > MAX_SIDE || height > MAX_SIDE) {
    fail(`dimensions ${width}x${height} exceed ${MAX_SIDE}x${MAX_SIDE}`);
  }
  if (!bytes.subarray(bytes.length - 12).includes(Buffer.from('IEND'))) {
    fail('no IEND chunk: image is truncated');
  }
  return { width, height };
}

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);
const { width, height } = checkPng(bytes);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
copyFileSync(source, target);
const written = statSync(target).size;
if (written !== bytes.length) fail('copy wrote a different number of bytes');
// Read the copy back and compare it byte for byte: a partial or
// corrupted write must never pass as a valid entry.
const writtenBytes = readFileSync(target);
if (!writtenBytes.equals(bytes)) fail('written file differs from entry.png');

console.log(`wrote ${target}: ${width}x${height} PNG, ${written} bytes`);
