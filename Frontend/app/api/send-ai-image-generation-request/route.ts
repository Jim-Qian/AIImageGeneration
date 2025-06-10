import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    console.log("Next.js API: Received AI image generation request:", body)

    // Get cookies from the browser request and forward them to Flask
    const cookieHeader = request.headers.get("cookie")
    console.log("Next.js API: Browser cookies:", cookieHeader)

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    }
    if (cookieHeader) {
      headers["Cookie"] = cookieHeader
    }

    // Forward the request to Flask with cookies
    const flaskResponse = await fetch("http://127.0.0.1:5000/api/sendAIImageGenerationRequest", {
      method: "POST",
      headers,
      body: JSON.stringify(body),
    })

    console.log("Next.js API: Flask AI generation response status:", flaskResponse.status)

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text()
      console.error("Next.js API: Flask returned error:", flaskResponse.status, errorText)
      return NextResponse.json(
        { status: "error", message: `Backend server error: ${flaskResponse.status}` },
        { status: flaskResponse.status },
      )
    }

    const data = await flaskResponse.json()
    console.log("Next.js API: Flask AI generation data:", data)

    return NextResponse.json(data)
  } catch (error) {
    console.error("Next.js API: Error with AI image generation:", error)
    return NextResponse.json({ status: "error", message: "Failed to connect to backend server" }, { status: 500 })
  }
}
