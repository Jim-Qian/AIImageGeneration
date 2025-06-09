import { type NextRequest, NextResponse } from "next/server"
import secrets from '../../../secrets.json';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    console.log("Next.js API: Received login request for:", body.username)

    // Forward the request to Flask
    const flaskResponse = await fetch(`${secrets.Backend_Server_URL}/api/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })

    console.log("Next.js API: Flask response status:", flaskResponse.status)

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text()
      console.error("Next.js API: Flask returned error:", flaskResponse.status, errorText)
      return NextResponse.json(
        { status: "error", message: `Backend server error: ${flaskResponse.status}` },
        { status: flaskResponse.status },
      )
    }

    const data = await flaskResponse.json()
    console.log("Next.js API: Flask response data:", data)

    // Create the response
    const response = NextResponse.json(data)

    // Forward Flask session cookies to the browser
    const setCookieHeader = flaskResponse.headers.get("set-cookie")
    if (setCookieHeader) {
      console.log("Next.js API: Forwarding session cookie:", setCookieHeader)
      response.headers.set("Set-Cookie", setCookieHeader)
    }

    return response
  } catch (error) {
    console.error("Next.js API: Error connecting to Flask:", error)
    return NextResponse.json({ status: "error", message: "Failed to connect to backend server" }, { status: 500 })
  }
}
