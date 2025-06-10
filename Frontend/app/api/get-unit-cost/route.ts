import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    console.log("Next.js API: Getting unit cost")

    // Forward the request to Flask
    const flaskResponse = await fetch("http://127.0.0.1:5000/api/getUnitCost", {
      method: "GET",
    })

    console.log("Next.js API: Flask unit cost response status:", flaskResponse.status)

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text()
      console.error("Next.js API: Flask returned error:", flaskResponse.status, errorText)
      return NextResponse.json(
        { status: "error", message: "Failed to get unit cost" },
        { status: flaskResponse.status },
      )
    }

    const data = await flaskResponse.json()
    console.log("Next.js API: Flask unit cost data:", data)

    return NextResponse.json(data)
  } catch (error) {
    console.error("Next.js API: Error getting unit cost from Flask:", error)
    return NextResponse.json({ status: "error", message: "Failed to connect to backend server" }, { status: 500 })
  }
}
