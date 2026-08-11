"use client";

import { useState } from "react";
import {
  ChevronDown,
  ChevronRight,
  FileCode2,
  Folder,
} from "lucide-react";

type TreeNode = {
  name: string;
  type: "file" | "folder";
  children?: TreeNode[];
};

const projectTree: TreeNode[] = [
  {
    name: "src",
    type: "folder",
    children: [
      {
        name: "devkit",
        type: "folder",
        children: [
          {
            name: "commands",
            type: "folder",
            children: [
              {
                name: "project.py",
                type: "file",
              },
              {
                name: "search.py",
                type: "file",
              },
            ],
          },
          {
            name: "core",
            type: "folder",
          },
          {
            name: "utils",
            type: "folder",
          },
          {
            name: "main.py",
            type: "file",
          },
          {
            name: "ui.py",
            type: "file",
          },
        ],
      },
    ],
  },
  {
    name: "tests",
    type: "folder",
  },
  {
    name: "README.md",
    type: "file",
  },
  {
    name: "pyproject.toml",
    type: "file",
  },
];

export default function ProjectTree() {
  return (
    <div className="space-y-1">
      {projectTree.map((node) => (
        <TreeItem
          key={node.name}
          node={node}
          level={0}
        />
      ))}
    </div>
  );
}

function TreeItem({
  node,
  level,
}: {
  node: TreeNode;
  level: number;
}) {
  const [open, setOpen] = useState(true);

  const isFolder = node.type === "folder";

  return (
    <div>
      <button
        onClick={() => {
          if (isFolder) {
            setOpen((current) => !current);
          }
        }}
        className="flex w-full items-center gap-2 rounded-lg py-2 pr-3 text-left text-sm text-zinc-300 transition hover:bg-white/5"
        style={{
          paddingLeft: `${level * 18 + 10}px`,
        }}
      >
        {isFolder ? (
          open ? (
            <ChevronDown className="h-4 w-4 text-zinc-600" />
          ) : (
            <ChevronRight className="h-4 w-4 text-zinc-600" />
          )
        ) : (
          <span className="w-4" />
        )}

        {isFolder ? (
          <Folder className="h-4 w-4 text-cyan-400" />
        ) : (
          <FileCode2 className="h-4 w-4 text-zinc-500" />
        )}

        <span>{node.name}</span>
      </button>

      {isFolder && open && node.children && (
        <div>
          {node.children.map((child) => (
            <TreeItem
              key={`${node.name}-${child.name}`}
              node={child}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}