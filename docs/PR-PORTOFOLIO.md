# PR — CINEMATIC RESUME PORTFOLIO

**Status:** ⏸️ PENDING
**Prioritas:** 🟡 MEDIUM
**Repo:** https://github.com/nexterade/nexterade.github.io
**Lokal:** ~/nexterade.github.io/

## Yang Perlu Dilakuin

1. Isi `data/resumeContent.js` — data pribadi (nexterade, LUMOSS, dll)
2. Ganti styling di `tailwind.config.js` — moss green theme
3. Fix hydration error di `app/layout.tsx`
4. Fix GSAP target error (`.project-stage-shell`, `.timeline-mobile-card`)
5. Deploy ke GitHub Pages
6. Update README LUMOSS — isi field Website

## Setup yang Udah Kelar

- [x] Fork repo Cinematic Resume
- [x] Clone ke Termux
- [x] Pindah ke home (~/) — fix symlink error
- [x] `npm install` sukses (96 packages, 0 vulnerabilities)
- [x] Preview lokal jalan: `npm run dev -- --webpack`

## Catatan Teknis

- Next.js 16.3.5 pake **Webpack** (Turbopack gak support Android/arm64)
- Dev server: `npm run dev -- --webpack`
- Hydration error karena font variable — bukan fatal
- GSAP error karena section kosong — fix setelah isi data