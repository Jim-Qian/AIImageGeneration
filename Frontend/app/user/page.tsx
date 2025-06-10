"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { User, Loader2 } from "lucide-react"

export default function UserPage() {
  const [username, setUsername] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const [mounted, setMounted] = useState(false)
  const [activeSection, setActiveSection] = useState("dashboard")
  const [balance, setBalance] = useState(0)
  const [unitCost, setUnitCost] = useState(0)
  const [size1, setSize1] = useState(512)
  const [size2, setSize2] = useState(512)
  const [prompt, setPrompt] = useState("")
  const [generatedImageUrl, setGeneratedImageUrl] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationError, setGenerationError] = useState("")
  const router = useRouter()

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!mounted) return

    async function checkAuth() {
      try {
        console.log("User page: Checking authentication")

        const response = await fetch("/api/check-auth")
        console.log("User page: Auth check response status:", response.status)

        const data = await response.json()
        console.log("User page: Auth check response data:", data)

        if (data.authenticated && data.user) {
          console.log("User page: User is authenticated:", data.user.username)
          setUsername(data.user.username)
          if (typeof window !== "undefined") {
            localStorage.setItem("user", JSON.stringify(data.user))
          }
          // Load balance and unit cost
          await loadBalance()
          await loadUnitCost()
        } else {
          console.log("User page: User is not authenticated, redirecting to login")
          router.push("/login")
        }
      } catch (err) {
        console.error("User page: Error checking authentication:", err)
        router.push("/login")
      } finally {
        setIsLoading(false)
      }
    }

    checkAuth()
  }, [router, mounted])

  const loadBalance = async () => {
    try {
      const response = await fetch("/api/get-balance")
      const data = await response.json()
      if (data.status === "success") {
        setBalance(data.balance)
      }
    } catch (error) {
      console.error("Error loading balance:", error)
    }
  }

  const loadUnitCost = async () => {
    try {
      const response = await fetch("/api/get-unit-cost")
      const data = await response.json()
      if (data.status === "success") {
        setUnitCost(data.unitCost)
      }
    } catch (error) {
      console.error("Error loading unit cost:", error)
    }
  }

  const handleLogout = async () => {
    try {
      console.log("User page: Logging out")
      await fetch("/api/logout")
      if (typeof window !== "undefined") {
        localStorage.removeItem("user")
      }
      router.push("/")
    } catch (err) {
      console.error("Error during logout:", err)
    }
  }

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setGenerationError("Please enter a prompt")
      return
    }

    // Add balance check
    if (balance < unitCost) {
      setGenerationError(`Insufficient balance. You need $${unitCost.toFixed(2)} but only have $${balance.toFixed(2)}`)
      return
    }

    setIsGenerating(true)
    setGenerationError("")
    setGeneratedImageUrl("")

    try {
      const response = await fetch("/api/send-ai-image-generation-request", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          size1: Number.parseInt(size1.toString()),
          size2: Number.parseInt(size2.toString()),
          prompt: prompt.trim(),
        }),
      })

      const data = await response.json()

      if (data.status === "success") {
        setGeneratedImageUrl(data.url)
        // Reload balance after generation
        await loadBalance()
      } else {
        setGenerationError(data.message || "Generation failed")
      }
    } catch (error) {
      console.error("Error generating image:", error)
      setGenerationError("Network error occurred")
    } finally {
      setIsGenerating(false)
    }
  }

  if (!mounted || isLoading) {
    return (
      <div className="min-h-screen bg-white flex flex-col">
        <header className="w-full h-16 border-b border-gray-200 flex items-center px-6">
          <div className="flex-1">
            <div className="h-6 bg-gray-200 rounded w-32 animate-pulse"></div>
          </div>
          <div className="h-10 w-10 bg-gray-200 rounded-full animate-pulse"></div>
        </header>
        <div className="flex-1 flex">
          <aside className="w-1/5 bg-gray-50 border-r border-gray-200 p-4">
            <div className="space-y-2">
              <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
              <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
            </div>
          </aside>
          <main className="flex-1 p-6">
            <div className="h-8 bg-gray-200 rounded w-64 mb-6 animate-pulse"></div>
            <div className="h-4 bg-gray-200 rounded w-full animate-pulse"></div>
          </main>
        </div>
      </div>
    )
  }

  const renderMainContent = () => {
    if (activeSection === "dashboard") {
      return (
        <div>
          <h2 className="text-2xl font-bold mb-6">Welcome, {username}!</h2>
          <p className="text-gray-600">
            This is your user dashboard. You can access your account information and settings from here.
          </p>
        </div>
      )
    }

    if (activeSection === "ai-generation") {
      return (
        <div>
          <div className="flex justify-between items-start mb-6">
            <h2 className="text-2xl font-bold">AI Image Generation</h2>
            <div className="text-right">
              <p className="text-sm text-gray-600">Current Balance</p>
              <p className={`text-xl font-semibold ${balance < unitCost ? "text-red-500" : "text-green-600"}`}>
                ${balance.toFixed(2)}
              </p>
              {balance < unitCost && <p className="text-xs text-red-500 mt-1">Insufficient funds</p>}
            </div>
          </div>

          <Card className="max-w-2xl">
            <CardHeader>
              <CardTitle>Generate AI Image</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Generated Image Display */}
              <div className="flex justify-center">
                <div className="w-64 h-64 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center bg-gray-50">
                  {isGenerating ? (
                    <div className="flex flex-col items-center space-y-2">
                      <Loader2 className="h-8 w-8 animate-spin text-gray-500" />
                      <p className="text-sm text-gray-500">Generating...</p>
                    </div>
                  ) : generatedImageUrl ? (
                    <img
                      src={generatedImageUrl || "/placeholder.svg"}
                      alt="Generated AI Image"
                      className="max-w-full max-h-full object-contain rounded"
                    />
                  ) : generationError ? (
                    <div className="text-center p-4">
                      <p className="text-red-500 text-sm">{generationError}</p>
                    </div>
                  ) : (
                    <div className="text-center">
                      <p className="text-gray-500 text-sm">Generated image will appear here</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Size Input */}
              <div className="flex items-center space-x-4">
                <Label className="w-16">Size:</Label>
                <div className="flex items-center space-x-2">
                  <Input
                    type="number"
                    value={size1}
                    onChange={(e) => setSize1(Number.parseInt(e.target.value) || 0)}
                    className="w-20"
                    min="1"
                    max="2000"
                  />
                  <span className="text-gray-500">x</span>
                  <Input
                    type="number"
                    value={size2}
                    onChange={(e) => setSize2(Number.parseInt(e.target.value) || 0)}
                    className="w-20"
                    min="1"
                    max="2000"
                  />
                </div>
              </div>

              {/* Prompt Input */}
              <div className="flex items-center space-x-4">
                <Label className="w-16">Prompt:</Label>
                <Input
                  type="text"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe the image you want to generate..."
                  className="flex-1"
                />
              </div>

              {/* Cost Display */}
              <div className="flex items-center space-x-4">
                <Label className="w-16">Cost:</Label>
                <span className="text-gray-700">${unitCost.toFixed(2)} per generation</span>
              </div>

              {/* Generate Button */}
              <div className="flex justify-end">
                <Button
                  onClick={handleGenerate}
                  disabled={isGenerating || !prompt.trim() || balance < unitCost}
                  className="px-8"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Generating...
                    </>
                  ) : balance < unitCost ? (
                    "Insufficient Balance"
                  ) : (
                    "Generate"
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )
    }

    return null
  }

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <header className="w-full h-16 border-b border-gray-200 flex items-center px-6">
        <div className="flex-1">
          <h1 className="text-xl font-semibold">My Website</h1>
        </div>
        <div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="rounded-full h-10 w-10 p-0">
                <User className="h-6 w-6" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <div className="px-2 py-1.5 text-sm font-medium border-b border-gray-100">{username}</div>
              <DropdownMenuItem onClick={handleLogout} className="cursor-pointer">
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      <div className="flex-1 flex">
        <aside className="w-1/5 bg-gray-50 border-r border-gray-200 p-4">
          <nav className="space-y-2">
            <div
              className={`px-3 py-2 rounded-md cursor-pointer ${
                activeSection === "dashboard" ? "bg-gray-100 font-medium" : "text-gray-600 hover:bg-gray-100"
              }`}
              onClick={() => setActiveSection("dashboard")}
            >
              Dashboard
            </div>
            <div
              className={`px-3 py-2 rounded-md cursor-pointer ${
                activeSection === "ai-generation" ? "bg-gray-100 font-medium" : "text-gray-600 hover:bg-gray-100"
              }`}
              onClick={() => setActiveSection("ai-generation")}
            >
              AI Image Generation
            </div>
          </nav>
        </aside>

        <main className="flex-1 p-6">{renderMainContent()}</main>
      </div>
    </div>
  )
}
