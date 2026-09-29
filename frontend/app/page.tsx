import Link from "next/link";

export default function Home() {
  return (
    <div>
      <Link href="/login">ログイン</Link>
      <br></br>
      <Link href="/pos">POS</Link>
    </div>
  )
}
