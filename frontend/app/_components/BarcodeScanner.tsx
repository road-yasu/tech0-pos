"use client";

import { useEffect, useState } from "react";
import { Html5Qrcode, Html5QrcodeSupportedFormats } from "html5-qrcode";

// カメラ映像を表示する領域のID
const REGION_ID = "barcode-scanner-region";

// 本のISBN（978 または 979 で始まる13桁）。下段の書籍JANコード（192〜）は弾く
const ISBN_PATTERN = /^97[89]\d{10}$/;

type Props = {
  onDetected: (isbn: string) => void; // 読み取れたISBNを親に渡す
  onClose: () => void; // 何も読まずに閉じる
};

export default function BarcodeScanner({ onDetected, onClose }: Props) {
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const scanner = new Html5Qrcode(REGION_ID, {
      formatsToSupport: [Html5QrcodeSupportedFormats.EAN_13], // 本のバーコード形式だけ読む
      verbose: false,
    });

    let detected = false; // 2回目以降の読み取りを無視するためのフラグ
    let startPromise: Promise<unknown> | null = null;

    // 開発モードでは useEffect が「実行→即片付け→再実行」されるため、
    // 起動を少しだけ遅らせて、1回目（すぐ片付けられる方）ではカメラを起動しない
    const timer = setTimeout(() => {
      startPromise = scanner
        .start(
          { facingMode: "environment" }, // スマホは背面カメラ。PCは使えるカメラに自動で切り替わる
          { fps: 10, qrbox: { width: 280, height: 120 } }, // バーコード向けの横長の読み取り枠
          (decodedText) => {
            if (detected) return;
            if (!ISBN_PATTERN.test(decodedText)) return;
            detected = true;
            onDetected(decodedText); // 親が閉じる → この部品が消える → 下の片付けでカメラ停止
          },
          () => {
            // 読み取れなかったフレームごとに呼ばれるので、何もしない
          },
        )
        .catch((err) => {
          console.error(err);
          setErrorMessage(
            "カメラを起動できませんでした。ブラウザのカメラ許可を確認してください。",
          );
        });
    }, 0);

    // 片付け：起動が終わるのを待ってからカメラを止める
    return () => {
      clearTimeout(timer);
      startPromise
        ?.then(() => (scanner.isScanning ? scanner.stop() : undefined))
        .catch((err) => console.error(err));
    };
    // 表示されたときに1回だけ起動したいので、依存配列は空にしている
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    // 画面全体を暗くして、中央にスキャナーを出す（モーダル）
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-sm space-y-3 rounded-lg bg-white p-4">
        <p className="text-center text-sm font-bold">
          本の裏の「上段」のバーコードを枠に合わせてください
        </p>
        <div id={REGION_ID} className="w-full overflow-hidden rounded" />
        {errorMessage && <p className="text-sm text-red-600">{errorMessage}</p>}
        <button
          onClick={onClose}
          className="w-full cursor-pointer rounded border border-gray-400 py-2 text-sm hover:bg-gray-100"
        >
          閉じる
        </button>
      </div>
    </div>
  );
}
