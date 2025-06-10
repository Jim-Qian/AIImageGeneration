import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    console.log("Next.js API: Getting user balance")

    // Get cookies from the browser request and forward them to Flask
    const cookieHeader = request.headers.get("cookie")
    console.log("Next.js API: Browser cookies:", cookieHeader)

    const headers: Record<string, string> = {}
    if (cookieHeader) {
      headers["Cookie"] = cookieHeader
    }

    // Forward the request to Flask with cookies
    const flaskResponse = await fetch("http://127.0.0.1:5000/api/getBalance", {
      method: "GET",
      headers,
    })

    console.log("Next.js API: Flask balance response status:", flaskResponse.status)

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text()
      console.error("Next.js API: Flask returned error:", flaskResponse.status, errorText)
      return NextResponse.json({ status: "error", message: "Failed to get balance" }, { status: flaskResponse.status })
    }

    const data = await flaskResponse.json()
    console.log("Next.js API: Flask balance data:", data)

    return NextResponse.json(data)
  } catch (error) {
    console.error("Next.js API: Error getting balance from Flask:", error)
    return NextResponse.json({ status: "error", message: "Failed to connect to backend server" }, { status: 500 })
  }
}
