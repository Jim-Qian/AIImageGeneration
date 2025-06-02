"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { User } from "lucide-react"

export default function UserPage() {
  const [username, setUsername] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const [mounted, setMounted] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!mounted) return

    async function checkAuth() {
      try {
        console.log("User page: Checking authentication")

        // Use Next.js API route (NOT direct Flask call)
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

  const handleLogout = async () => {
    try {
      console.log("User page: Logging out")
      // Use Next.js API route (NOT direct Flask call)
      await fetch("/api/logout")
      if (typeof window !== "undefined") {
        localStorage.removeItem("user")
      }
      router.push("/")
    } catch (err) {
      console.error("Error during logout:", err)
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
            <div className="px-3 py-2 rounded-md bg-gray-100 font-medium">Dashboard</div>
            <div className="px-3 py-2 rounded-md text-gray-600 hover:bg-gray-100 cursor-pointer">Profile</div>
            <div className="px-3 py-2 rounded-md text-gray-600 hover:bg-gray-100 cursor-pointer">Settings</div>
          </nav>
        </aside>

        <main className="flex-1 p-6">
          <h2 className="text-2xl font-bold mb-6">Welcome, {username}!</h2>
          <p className="text-gray-600">
            This is your user dashboard. You can access your account information and settings from here.
          </p>
        </main>
      </div>
    </div>
  )
}
