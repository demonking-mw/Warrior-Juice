"use client";

import type React from "react";
import { useState } from "react";
import { UserIcon, LockIcon } from "lucide-react";
import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/_components/elements/button";
import { Input } from "@/_components/elements/input";
import { Checkbox } from "@/_components/elements/checkbox";
import { set } from "zod";
import api from "@/_components/api_conn";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [googleCredential, setGoogleCredential] = useState();
  const router = useRouter();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Implement login logic here
    console.log("Login attempted with:", { username, password, rememberMe });
  };
  const handleGoogleLoginSuccess = (credentialResponse: any) => {
    if (credentialResponse.credential) {
      const decodedCredential = jwtDecode<any>(credentialResponse.credential);
      const currentTime = Math.floor(Date.now() / 1000);
      const { iat, exp } = decodedCredential;
      // Check if the credential is timely
      if (currentTime < iat || currentTime > exp) {
        console.log("Credential is not valid: expired or issued in the future");
      } else {
        setGoogleCredential(decodedCredential);
        console.log(decodedCredential);
        // send the jwt to backend for login
        try {
          const response = api.post("/users", {
            type: "go",
            jwt_token: credentialResponse.credential,
          });
          console.log("User created:", response);
        } catch (err) {
          console.error("Error creating user:", err);
        }
        router.push("/authredirect/landing"); // Redirects to /dashboard, to be replaced
      }
    } else {
      console.log("Credential is undefined");
    }
  };

  return (
    <GoogleOAuthProvider clientId="934728058727-jvm3keubjaluikeg06hl4voifiq8fcv0.apps.googleusercontent.com">
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-100 to-indigo-200 p-4 sm:p-6 md:p-8">
        <div className="w-1/2 max-w-md space-y-6 rounded-2xl bg-white p-4 shadow-lg sm:p-8">
          <h1 className="text-center text-2xl font-bold text-gray-800 sm:text-3xl">
            Welcome to W ~🧃
          </h1>
          <div className="mx-auto w-2/3 rounded-lg border border-black p-4">
            <form onSubmit={handleLogin} className="space-y-2 sm:space-y-4">
              <Input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                icon={<UserIcon className="h-5 w-5 text-gray-400" />}
              />
              <Input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                icon={<LockIcon className="h-5 w-5 text-gray-400" />}
              />
              <div className="flex flex-col space-y-2 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
                <a href="#" className="text-sm text-blue-600 hover:underline">
                  Forgot password?
                </a>
              </div>
              <Button type="submit" className="w-full">
                Log In
              </Button>
            </form>
          </div>
          <div className="mx-auto flex w-2/3 items-center justify-center rounded-lg border border-black p-4">
            <GoogleLogin
              onSuccess={handleGoogleLoginSuccess}
              onError={() => {
                console.log("Login Failed");
              }}
            />
          </div>

          <div className="mt-6 text-center text-sm text-gray-600 sm:mt-8">
            Don't have an account?{" "}
            <a href="#" className="text-blue-600 hover:underline">
              Sign up
            </a>
          </div>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
};

export default LoginPage;
