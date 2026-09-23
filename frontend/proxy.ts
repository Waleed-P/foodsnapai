import { NextResponse } from "next/server";

import type { NextRequest } from "next/server";

const authRoutes = ["/login", "/register"];

export function proxy(request: NextRequest) {
  const accessToken = request.cookies.get("access_token");

  const pathname = request.nextUrl.pathname;

  const isAuthPage = authRoutes.includes(pathname);

  if (!accessToken && pathname.startsWith("/home")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (accessToken && isAuthPage) {
    return NextResponse.redirect(new URL("/home", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/home/:path*", "/login", "/register"],
};
