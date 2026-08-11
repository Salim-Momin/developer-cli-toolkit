export default function Topbar() {
  return (
    <header className="flex h-20 items-center justify-between border-b border-white/10 px-8">
      <div>
        <p className="text-sm text-zinc-500">
          Developer Workspace
        </p>

        <h2 className="text-lg font-semibold text-white">
          Developer Command Center
        </h2>
      </div>

      <div className="flex items-center gap-3 rounded-full border border-emerald-400/20 bg-emerald-400/5 px-4 py-2">
        <span className="h-2 w-2 rounded-full bg-emerald-400" />

        <span className="text-xs text-emerald-300">
          DevKit Connected
        </span>
      </div>
    </header>
  );
}