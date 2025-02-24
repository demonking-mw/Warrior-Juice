"use client";

import type React from "react";
import { useState } from "react";
import { UserIcon, LockIcon } from "lucide-react";
import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";

import { Button } from "@/_components/elements/button";
import { Input } from "@/_components/elements/input";
import { Checkbox } from "@/_components/elements/checkbox";
import { set } from "zod";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [googleCredential, setGoogleCredential] = useState("");

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Implement login logic here
    console.log("Login attempted with:", { username, password, rememberMe });
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
              onSuccess={(credentialResponse) => {
                if (credentialResponse.credential) {
                    setGoogleCredential(jwtDecode(credentialResponse.credential));
                    console.log(jwtDecode(credentialResponse.credential));
                } else {
                  console.log("Credential is undefined");
                }
                
              }}
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
