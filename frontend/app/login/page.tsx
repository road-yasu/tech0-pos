"use client";

import { useState } from "react";
import { useFormState } from "react-dom";

export default function Login() {

    return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
         <div className="w-full max-w-md rounded-lg space-y-6 border border-gray-300 bg-white p-4 shadow-sm">
            <h1 className="text-center text-2xl font-bold">テクゼロン書店POS</h1>
        <form 
        className="flex flex-col gap-6"
        action="formAction">
            <div className="flex flex-col gap-1">
              <label htmlFor="userId" className="text-sm">ID</label>
              <input id="userId" type="text" className="rounded border border-gray-400 px-2 py-1" name="userId" required/>
            </div>
            <div className="flex flex-col gap-1">
              <label htmlFor="password" className="text-sm">パスワード</label>
              <input type="password" className="rounded border border-gray-400 px-2 py-1" name="password" required/>
            </div>
            <button id="password" type="submit" className="cursor-pointer rounded bg-blue-600 py-2 font-bold text-white hover:bg-blue-700">ログイン</button>
        </form>
        </div>
    </main>
    );
}