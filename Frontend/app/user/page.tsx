"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { User } from "lucide-react"

export default function UserPage() {
  const [username, setUsername] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    async function checkAuth() {
      try {
        const response = await fetch("http://localhost:5000/api/check-auth", {
          credentials: "include", // Important for cookies/session
        })

        const data = await response.json()

        if (data.authenticated) {
          setUsername(data.user.username)
          // Update local storage
          localStorage.setItem("user", JSON.stringify(data.user))
        } else {
          router.push("/login")
        }
      } catch (err) {
        console.error("Error checking authentication:", err)
        router.push("/login")
      } finally {
        setIsLoading(false)
      }
    }

    checkAuth()
  }, [router])

  const handleLogout = async () => {
    try {
      await fetch("http://localhost:5000/api/logout", {
        credentials: "include",
      })
      localStorage.removeItem("user")
      router.push("/")
    } catch (err) {
      console.error("Error during logout:", err)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
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
        {/* Sidebar - 20% width */}
        <aside className="w-1/5 bg-gray-50 border-r border-gray-200 p-4">
          <nav className="space-y-2">
            <div className="px-3 py-2 rounded-md bg-gray-100 font-medium">Dashboard</div>
            <div className="px-3 py-2 rounded-md text-gray-600 hover:bg-gray-100 cursor-pointer">Profile</div>
            <div className="px-3 py-2 rounded-md text-gray-600 hover:bg-gray-100 cursor-pointer">Settings</div>
          </nav>
        </aside>

        {/* Main content area */}
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
