import React from 'react';
import { AlertCircle, X } from 'lucide-react';

interface GenerationErrorProps {
    message: string;
    onDismiss?: () => void;
}

export const GenerationError: React.FC<GenerationErrorProps> = ({ message, onDismiss }) => (
    <div
        role="alert"
        aria-live="assertive"
        className="bg-red-50 border border-red-200 rounded-lg p-4 dark:bg-red-900/20 dark:border-red-500/30"
    >
        <div className="flex items-start">
            <div className="flex-shrink-0">
                <AlertCircle className="h-5 w-5 text-red-500 dark:text-red-400" aria-hidden="true" />
            </div>
            <div className="ml-3 flex-1">
                <h3 className="text-sm font-medium text-red-800 dark:text-red-300">Generation Error</h3>
                <div className="mt-1 text-sm text-red-700 dark:text-red-400">
                    <p>{message}</p>
                </div>
            </div>
            {onDismiss && (
                <div className="ml-auto pl-3">
                    <button
                        type="button"
                        onClick={onDismiss}
                        className="inline-flex rounded-md p-1.5 text-red-500 hover:bg-red-100 dark:text-red-400 dark:hover:bg-red-900/40 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-charcoal-900"
                        aria-label="Dismiss error message"
                    >
                        <X className="h-4 w-4" aria-hidden="true" />
                    </button>
                </div>
            )}
        </div>
    </div>
);
