import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    console.log("Next.js API: Logging out user")

    // Get cookies from the browser request and forward them to Flask
    const cookieHeader = request.headers.get("cookie")
    console.log("Next.js API: Browser cookies for logout:", cookieHeader)

    const headers: Record<string, string> = {}
    if (cookieHeader) {
      headers["Cookie"] = cookieHeader
    }

    // Forward the request to Flask with cookies
    const flaskResponse = await fetch("http://127.0.0.1:5000/api/logout", {
      method: "GET",
      headers,
    })

    console.log("Next.js API: Flask logout response status:", flaskResponse.status)

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text()
      console.error("Next.js API: Flask returned error:", flaskResponse.status, errorText)
      return NextResponse.json(
        { status: "error", message: `Backend server error: ${flaskResponse.status}` },
        { status: flaskResponse.status },
      )
    }

    const data = await flaskResponse.json()
    console.log("Next.js API: Flask logout data:", data)

    // Create the response
    const response = NextResponse.json(data)

    // Forward any cookie clearing headers from Flask
    const setCookieHeader = flaskResponse.headers.get("set-cookie")
    if (setCookieHeader) {
      console.log("Next.js API: Forwarding logout cookie:", setCookieHeader)
      response.headers.set("Set-Cookie", setCookieHeader)
    }

    return response
  } catch (error) {
    console.error("Next.js API: Error logging out with Flask:", error)
    return NextResponse.json({ status: "error", message: "Failed to connect to backend server" }, { status: 500 })
  }
}
