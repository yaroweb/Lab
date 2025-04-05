import "../styles/globals.css";
import { Inter } from "next/font/google";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Insolvy WebApp",
  description: "Insolvenzverfahren digital verwalten",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="de">
      <body className={cn(inter.className, "bg-white text-black")}>
        {children}
      </body>
    </html>
  );
}
