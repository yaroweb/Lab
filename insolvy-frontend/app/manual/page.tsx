'use client'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { useState } from 'react'

export default function ManualPage() {
  const [verwalter, setVerwalter] = useState('')
  const [datum, setDatum] = useState('')
  const [glaeubiger, setGlaeubiger] = useState('')

  const handleSubmit = async (e: any) => {
    e.preventDefault()
    await fetch('http://localhost:8000/manual', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        insolvenzverwalter: verwalter,
        datum_verfahrenseroeffnung: datum,
        glaeubiger,
      }),
    })
    alert('Eingabe gespeichert ✅')
    setVerwalter(''); setDatum(''); setGlaeubiger('')
  }

  return (
    <main className="p-4">
      <h1 className="text-xl font-semibold mb-4">✍️ Manuelle Dateneingabe</h1>
      <form onSubmit={handleSubmit} className="grid gap-4">
        <Input placeholder="Insolvenzverwalter" value={verwalter} onChange={(e) => setVerwalter(e.target.value)} />
        <Input placeholder="Datum Verfahrenseröffnung" type="date" value={datum} onChange={(e) => setDatum(e.target.value)} />
        <Textarea placeholder="Liste Gläubiger & Forderungen" rows={4} value={glaeubiger} onChange={(e) => setGlaeubiger(e.target.value)} />
        <Button type="submit">Speichern</Button>
      </form>
    </main>
  )
}
