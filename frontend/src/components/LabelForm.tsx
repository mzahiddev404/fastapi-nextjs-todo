// LabelForm component for creating and editing labels
import { useState } from "react";
import { Label, LabelCreate, LabelUpdate } from "@/types";
import { useLabels } from "@/hooks/useLabels";
import { Button, Input, Card, CardHeader, CardContent, Alert } from "@/components/ui";

interface LabelFormProps {
  label?: Label;
  onClose: () => void;
  onSuccess?: () => void;
}

const PREDEFINED_COLORS = [
  "#EF4444", // Red
  "#F97316", // Orange
  "#EAB308", // Yellow
  "#22C55E", // Green
  "#06B6D4", // Cyan
  "#3B82F6", // Blue
  "#8B5CF6", // Purple
  "#EC4899", // Pink
  "#6B7280", // Gray
  "#F59E0B", // Amber
];

export function LabelForm({ label, onClose, onSuccess }: LabelFormProps) {
  const [name, setName] = useState(label?.name || "");
  const [color, setColor] = useState(label?.color || PREDEFINED_COLORS[0]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const { createLabel, updateLabel } = useLabels();

  const isEditing = !!label;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const labelData: LabelCreate | LabelUpdate = {
        name: name.trim(),
        color,
      };

      if (isEditing) {
        await updateLabel(label.id, labelData as LabelUpdate);
      } else {
        await createLabel(labelData as LabelCreate);
      }

      onSuccess?.();
      onClose();
    } catch (err) {
      console.error("Label save error:", err);
      setError(err instanceof Error ? err.message : "Failed to save label. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <h3 className="text-lg font-medium text-gray-900">
          {isEditing ? "Edit Label" : "Create New Label"}
        </h3>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Label Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter label name"
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Color
            </label>
            <div className="flex flex-wrap gap-2">
              {PREDEFINED_COLORS.map((colorOption) => (
                <button
                  key={colorOption}
                  type="button"
                  onClick={() => setColor(colorOption)}
                  className={`w-8 h-8 rounded-full border-2 transition-all ${
                    color === colorOption
                      ? "border-gray-900 scale-110"
                      : "border-gray-300 hover:scale-105"
                  }`}
                  style={{ backgroundColor: colorOption }}
                  title={colorOption}
                />
              ))}
            </div>
            <div className="mt-2 flex items-center space-x-2">
              <span className="text-sm text-gray-500">Custom:</span>
              <input
                type="color"
                value={color}
                onChange={(e) => setColor(e.target.value)}
                className="w-8 h-8 rounded border border-gray-300 cursor-pointer"
              />
            </div>
          </div>

          {error && (
            <Alert variant="error">
              {error}
            </Alert>
          )}

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={onClose}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={isLoading}
              disabled={!name.trim()}
            >
              {isEditing ? "Update Label" : "Create Label"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
