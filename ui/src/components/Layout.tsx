import { NavLink, Outlet } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Sunrise, Beef, Bird, Lightbulb, LogOut, Languages } from 'lucide-react'
import { OfflineStatusIndicator } from '@/components/farmos/OfflineStatusIndicator'
import { OrigamiMark } from '@/components/farmos/OrigamiMark'
import { useAuth } from '@/context/AuthContext'
import { cn } from '@/lib/utils'

// RULE-UX-101 (Ch.13 §13.3): navigation flows outward from the Morning
// Briefing, not a generic dashboard menu.
export function Layout() {
  const { t, i18n } = useTranslation()
  const { user, logout } = useAuth()

  const navItems = [
    { to: '/', label: t('nav.briefing'), icon: Sunrise, end: true },
    { to: '/animals', label: t('nav.animals'), icon: Beef },
    { to: '/flocks', label: t('nav.flocks'), icon: Bird },
    { to: '/recommendations', label: t('nav.recommendations'), icon: Lightbulb },
  ]

  return (
    <div className="mx-auto flex min-h-svh max-w-5xl flex-col">
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-border bg-card px-4 py-3">
        <div className="flex items-center gap-2 text-lg font-bold text-primary">
          <OrigamiMark size={26} />
          {t('app.name')}
        </div>
        <div className="flex items-center gap-3">
          <OfflineStatusIndicator />
          <button
            onClick={() => i18n.changeLanguage(i18n.language === 'ar' ? 'en' : 'ar')}
            className="flex items-center gap-1 rounded-full px-2 py-1 text-sm text-muted-foreground hover:bg-muted"
            aria-label="Toggle language"
          >
            <Languages className="h-4 w-4" /> {i18n.language === 'ar' ? 'EN' : 'AR'}
          </button>
          {user && (
            <button onClick={logout} className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground">
              <LogOut className="h-4 w-4" /> {t('nav.logout')}
            </button>
          )}
        </div>
      </header>

      <nav className="flex gap-1 overflow-x-auto border-b border-border bg-card px-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-2 whitespace-nowrap border-b-2 px-4 py-3 text-sm font-medium',
                isActive ? 'border-primary text-primary' : 'border-transparent text-muted-foreground hover:text-foreground',
              )
            }
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <main className="flex-1 p-4">
        <Outlet />
      </main>
    </div>
  )
}
