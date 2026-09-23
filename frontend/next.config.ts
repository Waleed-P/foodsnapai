// import type { NextConfig } from "next";

// const nextConfig: NextConfig = {
//   /* config options here */
// };

// export default nextConfig;
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Your existing config options here */

  // Move it here, outside of the experimental block!
  allowedDevOrigins: ['localhost', '127.0.0.1', '*.local', '*'],

  experimental: {
    // Other experimental features go here if you have any
  },
};

export default nextConfig;