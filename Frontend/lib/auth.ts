// Helper functions for authentication

export async function checkAuthStatus() {
  try {
    const response = await fetch("/api/check-auth", {
      credentials: "include",
    })

    if (!response.ok) {
      throw new Error("Network response was not ok")
    }

    return await response.json()
  } catch (error) {
    console.error("Error checking auth status:", error)
    return { authenticated: false }
  }
}

export async function logout() {
  try {
    await fetch("/api/logout", {
      credentials: "include",
    })
    localStorage.removeItem("user")
    return true
  } catch (error) {
    console.error("Error during logout:", error)
    return false
  }
}
