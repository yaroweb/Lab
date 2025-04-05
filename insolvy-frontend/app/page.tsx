"use client";

export default function HomePage() {
  return (
    <main className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">📊 Willkommen bei Insolvy</h1>
      <p className="text-gray-700">
        Dies ist dein Dashboard für Insolvenzverfahren.
      </p>

      <ul className="mt-4 space-y-2">
        <li>
          <a className="underline text-blue-600" href="/upload">
            ⬆️ PDF Upload
          </a>
        </li>
        <li>
          <a className="underline text-blue-600" href="/manual">
            ✍️ Manuelle Eingabe
          </a>
        </li>
        <li>
          <a className="underline text-blue-600" href="/berater">
            💬 Insolvenzberater (Chat)
          </a>
        </li>
      </ul>
    </main>
  );
}
