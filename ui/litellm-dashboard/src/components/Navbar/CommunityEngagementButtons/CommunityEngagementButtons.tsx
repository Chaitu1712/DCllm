import { useDisableShowPrompts } from "@/app/(dashboard)/hooks/useDisableShowPrompts";
import { buttonVariants } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { cn } from "@/lib/cva.config";
import { Github, Slack } from "lucide-react";
import React from "react";

const COMMUNITY_LINKS = [
  {
    href: "https://www.litellm.ai/support",
    label: "Join Slack",
    tooltip: "Upstream Slack community",
    Icon: Slack,
  },
  {
    href: "https://github.com/Chaitu1712/DCllm",
    label: "DeepCloud LLM on GitHub",
    tooltip: "DeepCloud LLM on GitHub",
    Icon: Github,
  },
] as const;

export const CommunityEngagementButtons: React.FC = () => {
  const disableShowPrompts = useDisableShowPrompts();

  if (disableShowPrompts) {
    return null;
  }

  return (
    <TooltipProvider>
      <ButtonGroup aria-label="Community links">
        {COMMUNITY_LINKS.map(({ href, label, tooltip, Icon }) => (
          <Tooltip key={href}>
            <TooltipTrigger
              render={
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={label}
                  className={cn(buttonVariants({ variant: "outline", size: "icon" }), "text-muted-foreground")}
                />
              }
            >
              <Icon />
            </TooltipTrigger>
            <TooltipContent>{tooltip}</TooltipContent>
          </Tooltip>
        ))}
      </ButtonGroup>
    </TooltipProvider>
  );
};
