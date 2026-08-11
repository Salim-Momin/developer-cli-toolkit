"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import {
  Bot,
  FolderCode,
  GitBranch,
  Globe,
  LayoutDashboard,
  Search,
  Settings,
  Stethoscope,
  Terminal,
} from "lucide-react";

const navigation = [
  {
    name: "Dashboard",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Project",
    href: "/project",
    icon: FolderCode,
  },
  {
    name: "Search",
    href: "/search",
    icon: Search,
  },
  {
    name: "Git",
    href: "/git",
    icon: GitBranch,
  },
  {
    name: "API Tester",
    href: "/api-tester",
    icon: Globe,
  },
  {
    name: "Doctor",
    href: "/doctor",
    icon: Stethoscope,
  },
  {
    name: "AI Assistant",
    href: "/ai",
    icon: Bot,
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-white/10 bg-black">
      <div className="flex h-20 items-center gap-3 border-b border-white/10 px-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-400/30 bg-cyan-400/10">
          <Terminal className="h-5 w-5 text-cyan-400" />
        </div>

        <div>
          <h1 className="font-semibold tracking-wider text-white">
            DEVKIT
          </h1>

          <p className="text-xs text-zinc-500">
            Command Center
          </p>
        </div>
      </div>

      <nav className="flex-1 space-y-2 p-4">
        {navigation.map((item) => {
          const Icon = item.icon;

          const active =
            pathname === item.href ||
            (item.href !== "/" && pathname.startsWith(item.href));

          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm transition ${
                active
                  ? "bg-cyan-400/10 text-cyan-300"
                  : "text-zinc-400 hover:bg-white/5 hover:text-white"
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-white/10 p-4">
        <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-zinc-400 transition hover:bg-white/5 hover:text-white">
          <Settings className="h-4 w-4" />
          Settings
        </button>
      </div>
    </aside>
  );
}