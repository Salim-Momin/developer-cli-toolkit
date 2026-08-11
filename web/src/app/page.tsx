import {
  Activity,
  Code2,
  Files,
  GitBranch,
} from "lucide-react";

import Sidebar from "@/components/layout/sidebar";
import Topbar from "@/components/layout/topbar";
import StatCard from "@/components/dashboard/stat-card";

export default function Home() {
  return (
    <main className="flex min-h-screen bg-[#050505] text-white">
      <Sidebar />

      <section className="flex min-w-0 flex-1 flex-col">
        <Topbar />

        <div className="flex-1 overflow-y-auto p-8">
          <div className="mb-8">
            <p className="text-sm text-cyan-400">
              OVERVIEW
            </p>

            <h1 className="mt-2 text-3xl font-semibold tracking-tight">
              Project Intelligence
            </h1>

            <p className="mt-2 text-sm text-zinc-500">
              Inspect your project, development environment and workflow.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <StatCard
              title="Project Health"
              value="86/100"
              description="Healthy project structure"
              icon={Activity}
            />

            <StatCard
              title="Files"
              value="148"
              description="Across 31 directories"
              icon={Files}
            />

            <StatCard
              title="Primary Language"
              value="TypeScript"
              description="64 project files"
              icon={Code2}
            />

            <StatCard
              title="Git"
              value="Clean"
              description="Branch: main"
              icon={GitBranch}
            />
          </div>

          <div className="mt-6 grid gap-6 xl:grid-cols-[1.6fr_1fr]">
            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
              <div className="mb-6">
                <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">
                  Current project
                </p>

                <h2 className="mt-2 text-xl font-semibold">
                  PromptForgeAI
                </h2>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <Info
                  label="Framework"
                  value="Next.js"
                />

                <Info
                  label="Language"
                  value="TypeScript"
                />

                <Info
                  label="Git Repository"
                  value="Detected"
                />

                <Info
                  label="Tests"
                  value="Detected"
                />

                <Info
                  label="Docker"
                  value="Not detected"
                />

                <Info
                  label="Environment"
                  value=".env.example"
                />
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
              <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">
                Quick commands
              </p>

              <div className="mt-5 space-y-3">
                <Command text="devkit project info" />

                <Command text="devkit project health" />

                <Command text='devkit search "TODO"' />

                <Command text="devkit project tree" />
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

function Info({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-white/5 bg-black/20 p-4">
      <p className="text-xs text-zinc-500">
        {label}
      </p>

      <p className="mt-2 text-sm font-medium text-zinc-200">
        {value}
      </p>
    </div>
  );
}

function Command({
  text,
}: {
  text: string;
}) {
  return (
    <div className="rounded-xl border border-white/5 bg-black p-3 font-mono text-xs text-zinc-300">
      <span className="mr-2 text-cyan-400">$</span>
      {text}
    </div>
  );
}