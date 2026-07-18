interface HeaderProps {
  title: string;
  subtitle: string;
}

export default function Header({
  title,
  subtitle,
}: HeaderProps) {
  return (
    <header
      className="
        sticky top-0 z-20
        border-b border-white/40
        bg-white/65
        backdrop-blur-2xl
        shadow-[0_8px_30px_rgba(59,130,246,0.08)]
      "
    >
      <div className="mx-auto max-w-6xl px-8 py-3">

        <h1 className="text-3xl font-bold tracking-tight text-slate-900">
          {title}
        </h1>

        <p className="mt-1 text-sm text-slate-600">
          {subtitle}
        </p>

      </div>
    </header>
  );
}