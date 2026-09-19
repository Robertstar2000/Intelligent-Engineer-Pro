
import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { Project, User, Phase, Comment, Task } from '../types';
import { generateUUID } from '../utils/crypto';
import { setCustomApiKey } from '../services/geminiService';
import { db } from '../firebase';
import { doc, setDoc, collection, query, where, getDocs, deleteDoc, writeBatch } from 'firebase/firestore';

interface ProjectContextType {
    project: Project | null;
    setProject: React.Dispatch<React.SetStateAction<Project | null>>;
    projects: Project[];
    currentUser: User | null;
    setCurrentUser: React.Dispatch<React.SetStateAction<User | null>>;
    geminiKey: string;
    setGeminiKey: (key: string) => void;
    theme: string;
    setTheme: (theme: string) => void;
    
    // Auth & Project list management
    login: (email: string, pass: string) => Promise<boolean>;
    signup: (username: string, email: string, pass: string, geminiKey?: string) => Promise<string[] | false>;
    logout: () => void;
    updateUserProfile: (updates: Partial<User>) => void;
    
    // Project lifecycle management
    updateProject: (updatedProject: Project) => void;
    addProject: (newProject: Project) => void;
    deleteProject: (projectId: string) => void;
    deleteAllProjects: () => void;
    updateProjectDetails: (projectId: string, updates: { requirements: string, constraints: string }) => void;
    updatePhase: (projectId: string, phaseId: string, updates: Partial<Phase>) => void;
    addComment: (projectId: string, phaseId: string, text: string) => void;
    addTask: (projectId: string, task: Omit<Task, 'id' | 'createdAt'>) => void;
    updateTask: (projectId: string, updatedTask: Task) => void;
    updateCollaboratorEmails: (projectId: string, emails: string[]) => void;
    isLoading: boolean;
}

const ProjectContext = createContext<ProjectContextType | undefined>(undefined);

interface ProjectProviderProps {
    children?: ReactNode;
}

export const ProjectProvider = ({ children }: ProjectProviderProps) => {
    const [project, setProject] = useState<Project | null>(null);
    const [projects, setProjects] = useState<Project[]>([]);
    const [currentUser, setCurrentUser] = useState<User | null>(null);
    const [geminiKey, setGeminiKeyInternal] = useState(() => localStorage.getItem('hmap-gemini-api-key') || '');
    const [isLoading, setIsLoading] = useState(true);
    const [theme, setThemeState] = useState(() => {
        if (typeof window === 'undefined') return 'dark';
        return localStorage.getItem('theme') || 'dark';
    });

    const setTheme = (newTheme: string) => {
        if (newTheme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        localStorage.setItem('theme', newTheme);
        setThemeState(newTheme);
    };

    useEffect(() => {
        setTheme(theme);
    }, []);

    useEffect(() => {
        setCustomApiKey(geminiKey);
    }, [geminiKey]);

    const setGeminiKey = (key: string) => {
        setGeminiKeyInternal(key);
        setCustomApiKey(key);
        localStorage.setItem('hmap-gemini-api-key', key);
        if (currentUser) {
            updateUserProfile({ geminiKey: key });
        }
    };

    // Restore only a server-validated session; local user data alone never authenticates.
    useEffect(() => {
        fetch('/api/auth/me', { credentials: 'same-origin' }).then(async r => {
            if (!r.ok) throw new Error('expired');
            const { user } = await r.json();
            const mapped: User = { ...user, name: user.username, role: user.role || 'Engineer', avatar: user.avatar || '👤' };
            setCurrentUser(mapped);
            if (mapped.geminiKey) setGeminiKeyInternal(mapped.geminiKey);
            const q = query(collection(db, 'projects'), where('userId', '==', mapped.id));
            const snapshot = await getDocs(q);
            setProjects(snapshot.docs.map(item => item.data() as Project));
        }).catch(() => { setCurrentUser(null); }).finally(() => setIsLoading(false));
    }, []);

    const updateProject = async (updatedProject: Project) => {
        const normalizedProject = {
            ...updatedProject,
            disciplines: Array.isArray(updatedProject.disciplines) ? updatedProject.disciplines : Object.keys(updatedProject.disciplines || {})
        };
        setProjects(prevProjects => {
            const projectExists = prevProjects.some(p => p.id === normalizedProject.id);
            if (projectExists) {
                return prevProjects.map(p => p.id === normalizedProject.id ? normalizedProject : p);
            } else {
                return [...prevProjects, normalizedProject];
            }
        });
        if (project && project.id === normalizedProject.id) {
            setProject(normalizedProject);
        }
        // Persist to Firestore
        await setDoc(doc(db, 'projects', normalizedProject.id), normalizedProject);
    };

    const addProject = async (newProject: Project) => {
        const normalizedProject = {
            ...newProject,
            disciplines: Array.isArray(newProject.disciplines) ? newProject.disciplines : Object.keys(newProject.disciplines || {})
        };
        setProjects(prev => [...prev, normalizedProject]);
        await setDoc(doc(db, 'projects', normalizedProject.id), normalizedProject);
    };

    const deleteProject = async (projectId: string) => {
        setProjects(prev => prev.filter(p => p.id !== projectId));
        if (project?.id === projectId) {
            setProject(null);
        }
        await deleteDoc(doc(db, 'projects', projectId));
    };

    const deleteAllProjects = async () => {
        if (!currentUser) return;
        setProjects([]);
        setProject(null);
        const q = query(collection(db, 'projects'), where('userId', '==', currentUser.id));
        const querySnapshot = await getDocs(q);
        const batch = writeBatch(db);
        querySnapshot.docs.forEach(doc => batch.delete(doc.ref));
        await batch.commit();
    };

    const updateProjectDetails = async (projectId: string, updates: { requirements: string, constraints: string }) => {
        const updateFn = (p: Project) => p.id === projectId ? { ...p, ...updates } : p;
        
        let updatedProject: Project | undefined;
        setProjects(prev => {
            const next = prev.map(updateFn);
            updatedProject = next.find(p => p.id === projectId);
            return next;
        });
        
        if (project?.id === projectId) setProject(p => p ? updateFn(p) : null);
        
        if (updatedProject) {
            await setDoc(doc(db, 'projects', projectId), updatedProject);
        }
    };

    const updatePhase = async (projectId: string, phaseId: string, updates: Partial<Phase>) => {
        let updatedProject: Project | undefined;
        
        const updateFn = (p: Project) => {
            if (p.id === projectId) {
                const updatedPhases = p.phases.map(ph => ph.id === phaseId ? { ...ph, ...updates } : ph);
                updatedProject = { ...p, phases: updatedPhases };
                return updatedProject;
            }
            return p;
        };
        
        setProjects(prev => prev.map(updateFn));
        if (project?.id === projectId) setProject(p => p ? updateFn(p) : null);
        
        if (updatedProject) {
            await setDoc(doc(db, 'projects', projectId), updatedProject);
        }
    };

    const addComment = async (projectId: string, phaseId: string, text: string) => {
        if (!currentUser) return;
        const newComment: Comment = {
            id: generateUUID(),
            userId: currentUser.id,
            phaseId, text, createdAt: new Date()
        };
        
        let updatedProject: Project | undefined;
        const updateFn = (p: Project) => {
            if (p.id === projectId) {
                const updatedComments = { ...p.comments };
                if (!updatedComments[phaseId]) updatedComments[phaseId] = [];
                updatedComments[phaseId].push(newComment);
                updatedProject = { ...p, comments: updatedComments };
                return updatedProject;
            }
            return p;
        };
        
        setProjects(prev => prev.map(updateFn));
        if (project?.id === projectId) setProject(p => p ? updateFn(p) : null);
        
        if (updatedProject) {
            await setDoc(doc(db, 'projects', projectId), updatedProject);
        }
    };

    const addTask = async (projectId: string, task: Omit<Task, 'id' | 'createdAt'>) => {
         const newTask: Task = { ...task, id: generateUUID(), createdAt: new Date() };
         let updatedProject: Project | undefined;
         
         const updateFn = (p: Project) => {
            if (p.id === projectId) {
                const updatedTasks = [...(p.tasks || []), newTask];
                updatedProject = { ...p, tasks: updatedTasks };
                return updatedProject;
            }
            return p;
         };
         
         setProjects(prev => prev.map(updateFn));
         if (project?.id === projectId) setProject(p => p ? updateFn(p) : null);
         
         if (updatedProject) {
             await setDoc(doc(db, 'projects', projectId), updatedProject);
         }
    };

    const updateTask = async (projectId: string, updatedTask: Task) => {
        let updatedProject: Project | undefined;
        const updateFn = (p: Project) => {
            if (p.id === projectId) {
                const updatedTasks = (p.tasks || []).map(t => t.id === updatedTask.id ? updatedTask : t);
                updatedProject = { ...p, tasks: updatedTasks };
                return updatedProject;
            }
            return p;
        };
        setProjects(prev => prev.map(updateFn));
        if (project?.id === projectId) setProject(p => p ? updateFn(p) : null);
        
        if (updatedProject) {
            await setDoc(doc(db, 'projects', projectId), updatedProject);
        }
    };

    const updateCollaboratorEmails = async (projectId: string, emails: string[]) => {
        let updatedProject: Project | undefined;
        const updateFn = (p: Project) => {
            if (p.id === projectId) {
                updatedProject = { ...p, collaborators: emails };
                return updatedProject;
            }
            return p;
        };
        setProjects(prev => prev.map(updateFn));
        if (project?.id === projectId) setProject(p => p ? updateFn(p) : null);
        
        if (updatedProject) {
            await setDoc(doc(db, 'projects', projectId), updatedProject);
        }
    };

    const authPost = async (path: string, body: unknown) => {
        const { csrfToken } = await fetch('/api/auth/csrf', { credentials: 'same-origin' }).then(r => r.json());
        return fetch(path, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type':'application/json', 'X-CSRF-Token': csrfToken }, body: JSON.stringify(body) });
    };

    const login = async (email: string, pass: string): Promise<boolean> => {
        try {
            const response = await authPost('/api/auth/login', { emailOrUsername: email, password: pass });
            if (!response.ok) return false;
            const data = await response.json();
            setCurrentUser({ ...data.user, name: data.user.username, role: data.user.role || 'Engineer', avatar: data.user.avatar || '👤' });
            return true;
        } catch { return false; }
    };

    const signup = async (username: string, email: string, pass: string, geminiKey?: string): Promise<string[] | false> => {
        try {
            const response = await authPost('/api/auth/signup', { username, email, password: pass, geminiKey });
            if (!response.ok) return false;
            const data = await response.json();
            return data.recoveryCodes;
        } catch { return false; }
    };

    const updateUserProfile = async (updates: Partial<User>) => {
        if (!currentUser) return;
        const updatedUser = { ...currentUser, ...updates };
        setCurrentUser(updatedUser);
        await setDoc(doc(db, 'users', updatedUser.id), updatedUser);
    };

    const logout = async () => {
        await authPost('/api/auth/logout', {});
        setCurrentUser(null);
        setProject(null);
        setProjects([]);
    };

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-charcoal-900 text-gray-900 dark:text-white">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary"></div>
            </div>
        );
    }

    return (
        <ProjectContext.Provider value={{ 
            project, setProject, 
            projects,
            currentUser,
            setCurrentUser,
            geminiKey,
            setGeminiKey,
            theme, setTheme,
            login, signup, logout, updateUserProfile,
            updateProject, addProject, deleteProject, deleteAllProjects, updateProjectDetails, updatePhase, addComment, addTask, updateTask, updateCollaboratorEmails,
            isLoading
        }}>
            {children}
        </ProjectContext.Provider>
    );
};

export const useProject = (): ProjectContextType => {
    const context = useContext(ProjectContext);
    if (context === undefined) {
        throw new Error('useProject must be used within a ProjectProvider');
    }
    return context;
};
