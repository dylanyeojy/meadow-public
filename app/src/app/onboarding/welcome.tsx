import { View, StyleSheet, Text, ScrollView } from "react-native";
import { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { type, colors } from "@/theme";
import { router } from "expo-router";
import { PrimaryButton } from "@/components/primary-button";
import { ProgressBar } from "@/components/progress-bar";
import { PressableScale } from "@/components/pressable-scale";
import * as icons from "@/components/icons";

export default function OnboardingWelcomeScreen() {
    const [accepted, setAccepted] = useState(false);

    return (
        <SafeAreaView style={styles.screen}>
            <ProgressBar step={1} style={{ marginBottom: 26 }} />
            <ScrollView
                contentContainerStyle={styles.middle}
                keyboardShouldPersistTaps="handled"
                showsVerticalScrollIndicator={false}
            >
                <View style={styles.header}>
                    <Text style={styles.title}>
                        A gentle space to check in with yourself
                    </Text>
                    <Text style={styles.subtitle}>
                        Meadow helps you notice how you're doing over time.
                        Before we begin, a few things to understand.
                    </Text>
                </View>
                <View style={styles.disclaimerCard}>
                    <Text style={styles.cardHeading}>
                        Please read this first
                    </Text>
                    <Text style={styles.paragraph}>
                        Meadow is{" "}
                        <Text style={{ fontWeight: "bold" }}>
                            not a diagnostic tool
                        </Text>{" "}
                        and does not replace professional care. It can't
                        diagnose any condition, and nothing here is a substitute
                        for a doctor, counsellor, or emergency service.
                    </Text>
                    <Text style={styles.paragraph}>
                        Your check-ins and journal entries are stored to show
                        you your own trends. They stay private to your account.
                    </Text>
                    <Text style={styles.paragraph}>
                        When you write an entry, your journal text is sent
                        securely to an external AI provider to generate your
                        response.
                    </Text>
                    <Text style={[styles.paragraph, styles.lastParagraph]}>
                        If you're ever in crisis, we'll always show you 24/7
                        support lines.
                    </Text>
                </View>
                <View style={styles.checkBoxRow}>
                    <PressableScale
                        accessibilityRole="checkbox"
                        accessibilityState={{ checked: accepted }}
                        onPress={() => setAccepted(!accepted)}
                        hitSlop={{
                            top: 9,
                            bottom: 9,
                            left: 9,
                            right: 9,
                        }}
                    >
                        <View
                            style={[
                                styles.checkBox,
                                accepted && styles.boxTicked,
                            ]}
                        >
                            {accepted && (
                                <icons.CheckIcon
                                    color={colors.surface}
                                    size={15}
                                />
                            )}
                        </View>
                    </PressableScale>
                    <Text
                        onPress={() => setAccepted(!accepted)}
                        style={styles.agreementText}
                    >
                        I understand and accept the above.
                    </Text>
                </View>
            </ScrollView>
            <PrimaryButton
                label="I understand and accept"
                onPress={() => router.push("/onboarding/profile")}
                style={{ marginTop: 20 }}
                disabled={!accepted}
            />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: colors.sand,
        paddingHorizontal: 24,
        paddingTop: 8,
        paddingBottom: 45, // judge by eye.
    },
    middle: {
        flexGrow: 1,
    },
    header: {
        marginBottom: 28,
    },
    title: {
        ...type.title1,
        color: colors.ink,
        lineHeight: 34,
    },
    subtitle: {
        ...type.body,
        marginTop: 10,
        color: colors.muted,
    },
    disclaimerCard: {
        backgroundColor: colors.surface,
        borderWidth: 1,
        borderColor: colors.border,
        borderRadius: 20,
        padding: 20,
    },
    cardHeading: {
        ...type.headline,
        fontSize: 16,
        color: colors.ink,
        marginBottom: 10,
        includeFontPadding: false,
    },
    paragraph: {
        ...type.subhead,
        includeFontPadding: false,
        fontSize: 15,
        fontWeight: "400",
        lineHeight: 24,
        color: colors.ink,
        marginBottom: 12,
    },
    lastParagraph: {
        color: colors.muted,
        marginBottom: 0,
    },
    checkBoxRow: {
        flexDirection: "row",
        alignItems: "center",
        gap: 12,
        marginTop: 20,
    },
    checkBox: {
        width: 26,
        height: 26,
        borderRadius: 8,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: colors.surface,
        borderWidth: 1,
        borderColor: colors.border,
    },
    boxTicked: {
        backgroundColor: colors.sage,
    },
    agreementText: {
        ...type.subhead,
        color: colors.ink,
        fontSize: 15,
        fontWeight: "400",
        includeFontPadding: false,
    },
});
