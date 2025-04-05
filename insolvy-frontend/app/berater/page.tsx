'use client'
import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Loader2 } from 'lucide-react'

export default function BeraterPage() {
  const [frage, setFrage] = useState('')
  const [antwort, setAntwort] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChat = async () => {
    setLoading(true)
    setError('')
    setAntwort('')
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ frage }),
      })
      const data = await res.json()
      setAntwort(data.antwort)
    } catch (err: any) {
      setError('❌ Fehler beim Abrufen der Antwort')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="p-4 max-w-2xl mx-auto">
      <h1 className="text-xl font-semibold mb-4">💬 Insolvenzberater (LLM)</h1>
      <div className="space-y-4">
        <Input
          value={frage}
          onChange={(e) => setFrage(e.target.value)}
          placeholder="Stelle eine Frage zum Verfahren..."
        />
        <Button onClick={handleChat} disabled={loading || !frage}>
          {loading && <Loader2 className="animate-spin mr-2 h-4 w-4" />} Frage stellen
        </Button>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        {antwort && (
          <Card>
            <CardContent className="whitespace-pre-wrap p-4 text-sm text-gray-800">
              {antwort}
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  )
}
