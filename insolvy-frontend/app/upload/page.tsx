'use client'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Loader2 } from 'lucide-react'
import { Progress } from '@/components/ui/progress'

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(0)

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    setError('')
    setProgress(20)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      })
      setProgress(80)
      if (!res.ok) throw new Error('Upload fehlgeschlagen')
      setProgress(100)
      alert('✅ Datei erfolgreich verarbeitet')
    } catch (err: any) {
      setError(err.message || 'Unbekannter Fehler')
      setProgress(0)
    } finally {
      setUploading(false)
    }
  }

  return (
    <main className="p-4 max-w-xl mx-auto">
      <h1 className="text-xl font-semibold mb-4">⬆️ PDF-Datei hochladen</h1>
      <div className="space-y-4">
        <Input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <Button onClick={handleUpload} disabled={uploading} className="w-full">
          {uploading && <Loader2 className="animate-spin mr-2 h-4 w-4" />} Hochladen
        </Button>
        {uploading && <Progress value={progress} className="h-2" />}
        {error && <p className="text-red-600 text-sm">❌ {error}</p>}
      </div>
    </main>
  )
}
