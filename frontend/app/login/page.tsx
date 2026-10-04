"use client";

import { useActionState } from "react";
import { useRouter } from "next/navigation";

type LoginState = { error: string };

export default function Login() {
    const router = useRouter();

    async function loginAction(prev: LoginState, formData: FormData): Promise<LoginState> {
    // 1. formData.get("user_name") と formData.get("password") を取り出す
    const userName = formData.get("userName")
    const password = formData.get("password")
    const json = JSON.stringify({user_name: userName, password: password})
    // 2. POS画面と同じAPIのURLに、/login へ POST する（JSONで送る）
    try{
        const res = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            body: json,
            headers: {
                "Content-Type": "application/json",
            },
        });
        // 3. 401なら { error: "IDまたはパスワードが違います" } を返す
        //    それ以外の失敗なら { error: "ログインに失敗しました" } を返す
        const data = await res.json()
        if (data.status_code === 401) {
            return {error: "ユーザー名またはパスワードが違います"};
        }
        if (!res.ok) {
            return { error: "ログインに失敗しました" };
        }
        // 4. 成功したら、返ってきた user_id と user_name を sessionStorage に保存し、
        //    router.push("/pos") で移動する
        sessionStorage.setItem("userId", String(data.user_id));
        sessionStorage.setItem("userName", String(data.user_name));
        router.push("/pos");
        return {error: ""}
    } catch {
        return {error: "サーバーに接続できませんでした"};
        }
    }

    const [state, formAction, isPending] = useActionState(loginAction, { error: "" });

    return (
    <main className="flex min-h-screen items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-md space-y-6 rounded-lg border border-gray-300 bg-white p-4 shadow-sm">
        <h1 className="text-center text-2xl font-bold">テクゼロン書店POS</h1>
        <form className="flex flex-col gap-6" action={formAction}>
          <div className="flex flex-col gap-1">
            <label htmlFor="userName" className="text-sm">ユーザー名</label>
            <input id="userName" name="userName" type="text" required
              className="rounded border border-gray-400 px-2 py-1" />
          </div>
          <div className="flex flex-col gap-1">
            <label htmlFor="password" className="text-sm">パスワード</label>
            <input id="password" name="password" type="password" required
              className="rounded border border-gray-400 px-2 py-1" />
          </div>
          {state.error && <p className="text-sm text-red-600">{state.error}</p>}
          <button
            type="submit"
            disabled={isPending}
            className="cursor-pointer rounded bg-blue-600 py-2 font-bold text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {isPending ? "ログイン中…" : "ログイン"}
          </button>
        </form>
      </div>
    </main>
    );
}