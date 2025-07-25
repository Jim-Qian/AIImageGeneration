import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="min-h-screen bg-white flex flex-col">
      <header className="w-full h-16 border-b border-gray-200 flex items-center px-6">
        <div className="flex-1">
          <h1 className="text-xl font-semibold">My Website</h1>
        </div>
        <div className="flex gap-4">
          {/* Try using href instead of Link temporarily */}
          <a href="/register">
            <Button variant="outline">Register</Button>
          </a>
          <a href="/login">
            <Button>Login</Button>
          </a>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center p-6">
        <div className="max-w-2xl w-full text-center">
          <h2 className="text-3xl font-bold mb-6">Welcome to My Website</h2>
          <p className="text-gray-600 mb-8">
            This is the home page of our application. Please register or login to access your user dashboard.
          </p>
          <div className="flex gap-4 justify-center">
            {/* Try regular anchor tags */}
            <a href="/register">
              <Button variant="outline" size="lg">
                Create an account
              </Button>
            </a>
            <a href="/login">
              <Button size="lg">Sign in</Button>
            </a>
          </div>
        </div>
      </main>
    </div>
  )
}
