import {
  Activity,
  Box,
  Code2,
  Files,
  FolderTree,
} from "lucide-react";

import Sidebar from "@/components/layout/sidebar";
import Topbar from "@/components/layout/topbar";
import ProjectTree from "@/components/project-tree";

export default function ProjectPage() {
  return (
    <main className="flex min-h-screen bg-[#050505] text-white">
      <Sidebar />

      <section className="flex min-w-0 flex-1 flex-col">
        <Topbar />

        <div className="flex-1 overflow-y-auto p-8">
          <div className="mb-8">
            <p className="text-sm text-cyan-400">
              PROJECT
            </p>

            <h1 className="mt-2 text-3xl font-semibold tracking-tight">
              Project Explorer
            </h1>

            <p className="mt-2 text-sm text-zinc-500">
              Inspect structure, technology and project health.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <Metric
              icon={Activity}
              label="Health"
              value="85/100"
            />

            <Metric
              icon={Code2}
              label="Primary Language"
              value="Python"
            />

            <Metric
              icon={Files}
              label="Files"
              value="21"
            />

            <Metric
              icon={Box}
              label="Framework"
              value="Typer"
            />
          </div>

          <div className="mt-6 grid gap-6 xl:grid-cols-[1.25fr_1fr]">
            <section className="rounded-2xl border border-white/10 bg-white/[0.03]">
              <div className="flex items-center gap-3 border-b border-white/10 px-6 py-5">
                <FolderTree className="h-5 w-5 text-cyan-400" />

                <div>
                  <h2 className="font-medium">
                    Project Structure
                  </h2>

                  <p className="text-xs text-zinc-500">
                    developer-cli-toolkit
                  </p>
                </div>
              </div>

              <div className="p-4">
                <ProjectTree />
              </div>
            </section>

            <section className="space-y-6">
              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
                <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">
                  Project information
                </p>

                <div className="mt-5 space-y-3">
                  <Row label="Project" value="developer-cli-toolkit" />
                  <Row label="Type" value="Python CLI" />
                  <Row label="Framework" value="Typer + Rich" />
                  <Row label="Git" value="Detected" />
                  <Row label="Tests" value="Detected" />
                  <Row label="Docker" value="Not detected" />
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
                <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">
                  Languages
                </p>

                <div className="mt-5 space-y-4">
                  <Language
                    name="Python"
                    percentage={72}
                  />

                  <Language
                    name="Markdown"
                    percentage={15}
                  />

                  <Language
                    name="TOML"
                    percentage={8}
                  />

                  <Language
                    name="Other"
                    percentage={5}
                  />
                </div>
              </div>
            </section>
          </div>
        </div>
      </section>
    </main>
  );
}

function Metric({
  icon: Icon,
  label,
  value,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      <div className="mb-5 flex items-center justify-between">
        <p className="text-sm text-zinc-500">
          {label}
        </p>

        <Icon className="h-4 w-4 text-cyan-400" />
      </div>

      <p className="text-2xl font-semibold">
        {value}
      </p>
    </div>
  );
}

function Row({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between border-b border-white/5 pb-3 text-sm last:border-none">
      <span className="text-zinc-500">
        {label}
      </span>

      <span className="text-zinc-200">
        {value}
      </span>
    </div>
  );
}

function Language({
  name,
  percentage,
}: {
  name: string;
  percentage: number;
}) {
  return (
    <div>
      <div className="mb-2 flex justify-between text-xs">
        <span className="text-zinc-300">
          {name}
        </span>

        <span className="text-zinc-500">
          {percentage}%
        </span>
      </div>

      <div className="h-1.5 overflow-hidden rounded-full bg-white/5">
        <div
          className="h-full rounded-full bg-cyan-400"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>
    </div>
  );
}