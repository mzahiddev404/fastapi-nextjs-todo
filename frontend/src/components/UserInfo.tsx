"use client";

import { Card, CardHeader, CardContent } from "@/components/ui";
import { User } from "@/types";

interface UserInfoProps {
  user: User;
}

export function UserInfo({ user }: UserInfoProps) {
  return (
    <Card className="mt-6">
      <CardHeader>
        <h3 className="text-lg leading-6 font-medium text-gray-900">
          Account Information
        </h3>
      </CardHeader>
      <CardContent>
        <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">Name</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {user?.name || "Not provided"}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Email</dt>
            <dd className="mt-1 text-sm text-gray-900">{user?.email}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">User ID</dt>
            <dd className="mt-1 text-sm text-gray-900">{user?.id}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Status</dt>
            <dd className="mt-1 text-sm text-green-600">Authenticated</dd>
          </div>
        </dl>
      </CardContent>
    </Card>
  );
}
