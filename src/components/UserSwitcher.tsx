import React, { useState } from 'react';
import { useProject } from '../context/ProjectContext';
import { ChevronDown } from 'lucide-react';
import { InviteCollaboratorsModal } from './InviteCollaboratorsModal';

export const UserSwitcher = () => {
    const { project, currentUser, setCurrentUser } = useProject();
    const [isOpen, setIsOpen] = useState(false);
    const [isInviteModalOpen, setIsInviteModalOpen] = useState(false);

    React.useEffect(() => {
        if (!isOpen) return;
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === 'Escape') {
                setIsOpen(false);
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isOpen]);

    if (!project || !currentUser) return null;

    const handleSelect = (user: any) => {
        setCurrentUser(user);
        setIsOpen(false);
    };

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                aria-label="Switch current user"
                aria-expanded={isOpen}
                aria-haspopup="menu"
                className="flex items-center space-x-2 p-2 rounded-lg bg-gray-100 dark:bg-charcoal-800 hover:bg-gray-200 dark:hover:bg-charcoal-700 focus:outline-none focus:ring-2 focus:ring-brand-primary"
            >
                <span className="text-2xl">{currentUser.avatar}</span>
                <span className="font-medium text-sm hidden sm:inline">{currentUser.name}</span>
                <ChevronDown className="w-4 h-4 text-gray-500" />
            </button>
            {isOpen && (
                <div
                    role="menu"
                    aria-label="User switcher menu"
                    className="absolute right-0 mt-2 w-48 bg-white dark:bg-charcoal-800 border dark:border-charcoal-700 rounded-lg shadow-lg z-20"
                >
                    {project.users.map(user => (
                        <button
                            key={user.id}
                            role="menuitem"
                            onClick={() => handleSelect(user)}
                            className="w-full text-left flex items-center space-x-3 px-4 py-2 hover:bg-gray-100 dark:hover:bg-charcoal-700 focus:outline-none focus:bg-gray-100 dark:focus:bg-charcoal-700"
                        >
                            <span className="text-xl">{user.avatar}</span>
                            <span className="text-sm">{user.name}</span>
                        </button>
                    ))}
                    <div className="border-t dark:border-charcoal-700 mt-2 pt-2">
                        <button
                            role="menuitem"
                            onClick={() => { setIsInviteModalOpen(true); setIsOpen(false); }}
                            className="w-full text-left px-4 py-2 text-sm text-brand-primary hover:bg-gray-100 dark:hover:bg-charcoal-700 focus:outline-none focus:bg-gray-100 dark:focus:bg-charcoal-700"
                        >
                            Invite Collaborators
                        </button>
                    </div>
                </div>
            )}
            {isInviteModalOpen && <InviteCollaboratorsModal onClose={() => setIsInviteModalOpen(false)} />}
        </div>
    );
};
