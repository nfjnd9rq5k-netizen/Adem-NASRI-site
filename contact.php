<?php
/**
 * Reception du formulaire de contact de adem-nasri.fr.
 *
 * Repond en JSON quand le navigateur le demande (cas normal, via contact.js),
 * et par une redirection quand le formulaire est poste sans JavaScript.
 * L'expediteur est une adresse du domaine : envoyer « depuis » l'adresse du
 * visiteur ferait echouer SPF et le message finirait en indesirable.
 */
declare(strict_types=1);

const DESTINATAIRE = 'nasri.adem@hotmail.fr';
const EXPEDITEUR   = 'contact@adem-nasri.fr';
const SUJETS       = ['Mission', 'Recrutement', 'Café tech', 'Autre'];
const MAX_PAR_HEURE = 5;

// ---------------------------------------------------------------- utilitaires
function veut_json(): bool {
    $a = $_SERVER['HTTP_ACCEPT'] ?? '';
    return strpos($a, 'application/json') !== false
        || ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '') === 'fetch';
}

function repondre(int $code, array $data, string $ancre = '') {
    if (veut_json()) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        header('X-Content-Type-Options: nosniff');
        echo json_encode($data, JSON_UNESCAPED_UNICODE);
    } else {
        header('Location: /contact/' . $ancre, true, 303);
    }
    exit;
}

/** Limite simple par IP : au-dela de MAX_PAR_HEURE envois, on refuse. */
function trop_de_messages(): bool {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'inconnue';
    $f  = sys_get_temp_dir() . '/an-contact-' . md5($ip) . '.txt';
    $maintenant = time();
    $envois = [];
    if (is_readable($f)) {
        $envois = array_filter(
            array_map('intval', explode(',', (string)file_get_contents($f))),
            static function (int $t) use ($maintenant) { return $t > $maintenant - 3600; }
        );
    }
    if (count($envois) >= MAX_PAR_HEURE) {
        return true;
    }
    $envois[] = $maintenant;
    @file_put_contents($f, implode(',', $envois), LOCK_EX);
    return false;
}

// ---------------------------------------------------------------- traitement
$methode = $_SERVER['REQUEST_METHOD'] ?? '';

// Un humain qui tape l'adresse du script dans sa barre est renvoye vers le
// formulaire. Toute autre methode que POST est refusee franchement, sans
// redirection : un 303 a la place d'un 405 masque l'erreur a un client.
if ($methode === 'GET' || $methode === 'HEAD') {
    header('Location: /contact/', true, 303);
    exit;
}
if ($methode !== 'POST') {
    http_response_code(405);
    header('Allow: POST');
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['ok' => false, 'erreur' => 'methode'], JSON_UNESCAPED_UNICODE);
    exit;
}

// Champ piege : invisible pour un humain, rempli par les robots.
// On repond « ok » sans rien envoyer, pour ne pas leur indiquer la parade.
if (trim((string)($_POST['site_web'] ?? '')) !== '') {
    repondre(200, ['ok' => true], '?envoye=1');
}

$nom     = trim((string)($_POST['name'] ?? ''));
$email   = trim((string)($_POST['email'] ?? ''));
$sujet   = trim((string)($_POST['subject'] ?? 'Autre'));
$message = trim((string)($_POST['message'] ?? ''));

if (!in_array($sujet, SUJETS, true)) {
    $sujet = 'Autre';
}

$champs = [];
if ($nom === '' || mb_strlen($nom) > 120)            { $champs[] = 'name'; }
if (!filter_var($email, FILTER_VALIDATE_EMAIL))       { $champs[] = 'email'; }
if ($message === '' || mb_strlen($message) > 5000)    { $champs[] = 'message'; }
if ($champs !== []) {
    repondre(422, ['ok' => false, 'champs' => $champs]);
}

// Un retour a la ligne dans ces champs permettrait d'injecter des en-tetes.
foreach ([$nom, $email, $sujet] as $valeur) {
    if (preg_match('/[\r\n]/', $valeur)) {
        repondre(400, ['ok' => false, 'erreur' => 'entetes']);
    }
}

if (trop_de_messages()) {
    repondre(429, ['ok' => false, 'erreur' => 'trop_de_messages']);
}

$corps = "Nouveau message depuis adem-nasri.fr\n\n"
       . "Nom    : {$nom}\n"
       . "Email  : {$email}\n"
       . "Sujet  : {$sujet}\n"
       . "Date   : " . date('d/m/Y à H:i') . "\n"
       . "IP     : " . ($_SERVER['REMOTE_ADDR'] ?? 'inconnue') . "\n\n"
       . str_repeat('-', 46) . "\n\n"
       . $message . "\n\n"
       . str_repeat('-', 46) . "\n"
       . "Repondre a ce message ecrira directement a {$email}.\n";

$objet = '=?UTF-8?B?' . base64_encode("[adem-nasri.fr] {$sujet} — {$nom}") . '?=';

$entetes = implode("\r\n", [
    'From: Site adem-nasri.fr <' . EXPEDITEUR . '>',
    'Reply-To: ' . mb_encode_mimeheader($nom, 'UTF-8') . ' <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
]);

$envoye = @mail(DESTINATAIRE, $objet, $corps, $entetes, '-f' . EXPEDITEUR);

if (!$envoye) {
    error_log('[contact] echec mail() pour ' . $email);
    repondre(500, ['ok' => false, 'erreur' => 'envoi']);
}

repondre(200, ['ok' => true], '?envoye=1');
