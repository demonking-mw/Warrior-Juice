import "~/styles/globals.css";

import { GeistSans } from "geist/font/sans";
import { type Metadata } from "next";

import { TRPCReactProvider } from "~/trpc/react";
import Link from "next/link";

function Header() {
  return (
    <header className ="bg-black py-1">
      <div className ="container mx-auto px-10">
        <nav className ="flex items-center justify-between text-yellow-500 font-semibold">
          <div className = "flex items-center">
            <Link href="/">Home</Link>
          </div>
          <div>
            <Link href="/testroute">Route</Link>
          </div>
          <div>
            <Link href="/testroute2">Route2</Link>
          </div>
        </nav>
      </div>
    </header>
  )
}

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${GeistSans.variable}`}>
      <body>
        <TRPCReactProvider>
          <Header />
          {children}</TRPCReactProvider>
      </body>
    </html>
  );
}
