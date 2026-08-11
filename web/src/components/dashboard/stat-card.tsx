import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  description: string;
  icon: LucideIcon;
}

export default function StatCard({
  title,
  value,
  description,
  icon: Icon,
}: StatCardProps) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      <div className="mb-5 flex items-center justify-between">
        <p className="text-sm text-zinc-400">
          {title}
        </p>

        <div className="rounded-lg bg-white/5 p-2">
          <Icon className="h-4 w-4 text-cyan-300" />
        </div>
      </div>

      <p className="text-3xl font-semibold text-white">
        {value}
      </p>

      <p className="mt-2 text-xs text-zinc-500">
        {description}
      </p>
    </div>
  );
}